from __future__ import annotations

import os
import random
import shutil
from copy import deepcopy

import requests.exceptions
from slugify import slugify

from firebase.firestore import Firestore
from nlp.config import SOURCE_LANG_FROM_TARGET, SOURCE_LANGUAGE, TRANSLATION_MODEL, IMPROVED, IMPROVED_TITLE
from nlp.languages import SPANISH, ENGLISH
from nlp.mistral_7b import Mistral7B
from nlp.llama_3 import Llama3
from nlp.translator import Translator
from scrapers.FilmAffinity_parsers import extract_info_from_movie_page, get_translated_titles_film_affinity_languages, \
    clean_name, clean_translated_synopsis
from scrapers.constants.FilmAffinity_films_inspector import FILMS_DATABASE_JSON_PATH, STORED_IDS_JSON_PATH, \
    PENDING_FILMS_JSON_PATH, DISCARDED_IDS_JSON_PATH
from scrapers.constants.FilmAffinity import URL, ID, TITLE, COUNTRY, YEAR, FIRST_FILM_AFFINITY_YEAR, \
    InvalidMovieException, PENDING_TO_TRANSLATE, SYNOPSIS, LANGUAGES, BASIC_INFO, ORIGINAL_TITLE, \
    TRANSLATIONS_BATCH_SIZE, BACKUP_FILM_DATABASE_EVERY, FILM_AFFINITY_SYNOPSIS, SLUG, REPHRASED_SYNOPSIS, \
    SHORT_SYNOPSIS

from scrapers.FilmAffinity_link_discoverer import FilmAffinityLinkDiscoverer
import json
from loguru import logger
from tqdm import tqdm


class FilmAffinityFilmsInspector(FilmAffinityLinkDiscoverer):
    """
    Class that extract all the information
    """
    def __init__(self):
        super().__init__()
        if not os.path.exists(FILMS_DATABASE_JSON_PATH):
            logger.warning(f"Films database not found. Creating new one")
            with open(FILMS_DATABASE_JSON_PATH, "w") as f:
                json.dump({}, f)
        self.inverse_countries = {v: k for k, v in self.countries.items()}
        self.inverse_genres = {v: k for k, v in self.main_genres.items()}

        self.firestore_client = Firestore()
        # Get the known films
        #self.pending_films = json.load(open(FILMS_DATABASE_JSON_PATH, "r", encoding="utf-8"))
        self.pending_films = json.load(open(PENDING_FILMS_JSON_PATH, "r", encoding="utf-8"))

        self.stored_ids = json.load(open(STORED_IDS_JSON_PATH, "r", encoding="utf-8"))
        self.discarded_films = json.load(open(DISCARDED_IDS_JSON_PATH, "r", encoding="utf-8"))

        self.llm_rephraser = Mistral7B()


    def fill_pending_films(self, save_every: int = BACKUP_FILM_DATABASE_EVERY) -> None:
        """
        Fill the film database with all the films from FilmAffinity
        :param from_year: Year from which to start the search. If None, it will start from the last year inspected
        """
        film_ids = self.get_non_inspected_film_ids()
        for i, film_id in enumerate(film_ids):
            film_info = self.discovered_links_database[film_id]
            slug = slugify(film_info[TITLE])
            try:
                film_db_entry = self.extract_info_from_film(film_info=film_info, _id=film_id)
            except AssertionError as e:
                if "award type:" in str(e):
                    logger.error(f"Omitted error: {e}")
                    continue
                raise e

            if film_db_entry is None:
                self.discarded_films[film_id] = slug
                continue

            self.pending_films[film_id] = film_db_entry

            if i % save_every == 0 and i > 0:
                logger.info(f"Backing database up")
                self.backup_database()

    def backup_database(self, verbose:bool = True) -> None:
        """
        Backup the database to a json file
        """
        #super().backup_database(verbose=verbose)
        # Save all of them
        with open(PENDING_FILMS_JSON_PATH, "w", encoding="utf-8") as file:
            json.dump(self.pending_films, file, indent=4, ensure_ascii=False)
        with open(DISCARDED_IDS_JSON_PATH, "w", encoding="utf-8") as file:
            json.dump(self.discarded_films, file, indent=4, ensure_ascii=False)


        if len(self.pending_films) < TRANSLATIONS_BATCH_SIZE:
            logger.info(f"Not enough pending translations to start translating. Pending translations: {len(self.pending_films)}")
            return

        self.fill_all_pending_translations()

        # Write it on firestore
        self.firestore_client.insert_batch(data=self.pending_films)
        for film_id in list(self.pending_films.keys()):
            assert film_id not in self.stored_ids, f"ID {film_id} was already stored?"
            self.stored_ids[film_id] = self.pending_films.pop(film_id)[SLUG]
        assert len(self.pending_films) == 0, f"All pending films should have been stored in firestore. But there are still {len(self.pending_films)}"

        with open(PENDING_FILMS_JSON_PATH, "w", encoding="utf-8") as file:
            json.dump(self.pending_films, file, indent=4, ensure_ascii=False)
        with open(STORED_IDS_JSON_PATH, "w", encoding="utf-8") as file:
            json.dump(self.stored_ids, file, indent=4, ensure_ascii=False)
        """
        # First copy the current json file to a temp file
        temp_file = FILMS_DATABASE_JSON_PATH + ".temp"
        shutil.copyfile(FILMS_DATABASE_JSON_PATH, temp_file)
        # Then overwrite the json file with the new data
        try:
            with open(FILMS_DATABASE_JSON_PATH, "w", encoding="utf-8") as file:
                json.dump(self.pending_films, file, indent=4, ensure_ascii=False)
        except Exception as e:
            # If something goes wrong, restore the old json file
            shutil.copyfile(temp_file, FILMS_DATABASE_JSON_PATH)
            raise e
        # Finally remove the temp file
        os.remove(temp_file)
        """
        if verbose:
            logger.info(f"Films Database backed up. Films inspected: {len(self.discarded_films) + len(self.stored_ids)}/{len(self.discovered_links_database)}")


    def extract_info_from_film(self, film_info: dict[str, str], _id: str) -> dict[str, dict | str] | None:
        """
        Extract all the FilmAffinity information from a film
        :param film_info: Film information
        :return: dict with the film information
        """
        html = self.get(url=film_info[URL])
        try:
            movie_info = extract_info_from_movie_page(html=html, countries_inverse_dict=self.inverse_countries,
                                                genres_inverse_dict=self.inverse_genres, card_info=film_info)
            movie_info = self.include_synopsis_rephrasing(movie_info = movie_info)

            movie_info[ID] = _id
            return movie_info
        except InvalidMovieException as e:
            logger.warning(f"Deleted an invalid entry: {film_info[TITLE]} (URL: {film_info[URL]})")
            logger.warning(f"Error: {e}")
            # Delete it from the database
            self.discovered_links_database.pop(_id)
            return None
        except requests.exceptions.ReadTimeout:
            logger.warning(f"Timeout error while extracting info from {film_info[TITLE]} (URL: {film_info[URL]})")
            return None

    def include_synopsis_rephrasing(self, movie_info: dict):
        film_affinity_synopsis = deepcopy(movie_info[FILM_AFFINITY_SYNOPSIS])
        for lang in (ENGLISH, SPANISH):
            film_affinity_synopsis[lang][SYNOPSIS] = self.llm_rephraser.rephrase(film_affinity_synopsis_info=film_affinity_synopsis,
                                                                                 lang=lang)
            film_affinity_synopsis[lang][SHORT_SYNOPSIS] = self.llm_rephraser.get_synopsis_summary(film_affinity_synopsis_info=film_affinity_synopsis,
                                                                                 lang=lang)

        movie_info[PENDING_TO_TRANSLATE] = film_affinity_synopsis
        return movie_info

    def get_non_inspected_film_ids(self) -> list[str]:
        """
        Get the film ids that are not in the database
        """

        # Get the film ids from the search
        non_inspected_film_ids = set(self.discovered_links_database.keys()) - set(list(self.stored_ids.keys()) + list(self.discarded_films.keys()) + list(self.pending_films.keys()))

        non_inspected_film_ids = list(non_inspected_film_ids)
        random.shuffle(non_inspected_film_ids)
        return non_inspected_film_ids

    def fill_all_pending_translations(self, batch_size: int = TRANSLATIONS_BATCH_SIZE) -> None:
        """
        Translate all the pending translations
        :param batch_size: Number of translations to do in each batch. It will not start translating anything if there are
        less than batch_size pending translations
        """
        # Get all the films_ids with pending translations
        films_ids = tuple(str(film_id) for film_id, film_info in self.pending_films.items() if PENDING_TO_TRANSLATE in film_info)
        if len(films_ids) < batch_size:
            logger.info(f"Not enough pending translations to start translating. Pending translations: {len(films_ids)}")
            return
        # Unload Mistral7B to left GPU space for the new models
        self.llm_rephraser.unload_model()
        self.translate_synopsis_with_only_one_language(films_ids=films_ids)
        translated_titles = {film_id: get_translated_titles_film_affinity_languages(original_languages=self.pending_films[film_id][PENDING_TO_TRANSLATE])
                             for film_id in tqdm(films_ids, desc="Translating titles")}
        with tqdm(total=len(films_ids)*len(SOURCE_LANG_FROM_TARGET), desc="Translated Sentences") as pbar:
            for target, source in SOURCE_LANG_FROM_TARGET.items():
                with Translator(lang_pair=(source, target)) as translator:
                    for film_id in films_ids:
                        if LANGUAGES not in self.pending_films[film_id]:
                            self.pending_films[film_id][LANGUAGES] = {}
                        assert target not in self.pending_films[film_id][LANGUAGES]
                        original_languages = self.pending_films[film_id][PENDING_TO_TRANSLATE]
                        original_title = self.pending_films[film_id][BASIC_INFO][ORIGINAL_TITLE]
                        if target in original_languages:
                            title = original_languages[target][TITLE]
                        else:
                            if translated_titles[film_id][source] is None:
                                title = original_title
                            else:
                                title, reliable = translator.translate(text=translated_titles[film_id][source])
                                if not reliable:
                                    title = original_title

                        synopsis = original_languages[source][SYNOPSIS]
                        if synopsis is not None:
                            synopsis, reliable = translator.translate(text=synopsis)
                            synopsis = clean_name(synopsis, reencode=True)
                            synopsis = clean_translated_synopsis(synopsis)
                            if not synopsis.endswith("."):
                                synopsis = f"{synopsis}."
                        assert title is not None, f"Title is None for language {target}"
                        
                        short_synopsis = original_languages[source][SHORT_SYNOPSIS]
                        if short_synopsis is not None:
                            short_synopsis, reliable = translator.translate(text=short_synopsis)
                            short_synopsis = clean_name(short_synopsis, reencode=True)
                            short_synopsis = clean_translated_synopsis(short_synopsis)
                            if not short_synopsis.endswith("."):
                                short_synopsis = f"{short_synopsis}."
                        
                        self.pending_films[film_id][LANGUAGES][target] = {TITLE: clean_name(title, reencode=True),
                                                                          SYNOPSIS: synopsis,
                                                                          SHORT_SYNOPSIS: short_synopsis,
                                                                          SOURCE_LANGUAGE: source,
                                                                          TRANSLATION_MODEL: translator._model_name,
                                                                          IMPROVED: False,
                                                                          IMPROVED_TITLE: False}
                        pbar.update(1)

        assert all(len(self.pending_films[film_id][LANGUAGES]) == len(SOURCE_LANG_FROM_TARGET) for film_id in films_ids), \
            "Not all the languages have been translated"
        for film_id in films_ids:
            self.pending_films[film_id][REPHRASED_SYNOPSIS] = self.pending_films[film_id].pop(PENDING_TO_TRANSLATE)
        assert all(PENDING_TO_TRANSLATE not in self.pending_films[film_id] for film_id in self.pending_films), \
            "Not all the pending translations have been removed"



    def translate_synopsis_with_only_one_language(self, films_ids: tuple[str]) -> None:
        translate_to = {SPANISH: [], ENGLISH: []}
        for film_id in films_ids:
            assert all(language in (SPANISH, ENGLISH) for language in self.pending_films[film_id][PENDING_TO_TRANSLATE]), \
                f"Invalid language in pending translations: {self.pending_films[film_id][PENDING_TO_TRANSLATE]}"
            have_sinopsis = {lang: info[SYNOPSIS] is not None for lang, info in
                             self.pending_films[film_id][PENDING_TO_TRANSLATE].items()}
            if have_sinopsis[SPANISH] and not have_sinopsis[ENGLISH]:
                translate_to[ENGLISH].append(film_id)
            elif have_sinopsis[ENGLISH] and not have_sinopsis[SPANISH]:
                translate_to[SPANISH].append(film_id)
            # translated_titles = get_translated_titles_film_affinity_languages(original_languages=self.films_database[film_id][PENDING_TO_TRANSLATE])
        if any(len(synopsis) for synopsis in translate_to.values()) > 0:
            for target_lang, film_ids_to_translate in translate_to.items():
                if len(film_ids_to_translate) > 0:
                    src_lang = SOURCE_LANG_FROM_TARGET[target_lang]
                    with Translator(lang_pair=(src_lang, target_lang)) as translator:
                        for film_id in film_ids_to_translate:
                            src_synopsis = self.pending_films[film_id][PENDING_TO_TRANSLATE][src_lang][SYNOPSIS]
                            assert src_synopsis is not None, f"Synopsis is None for film {film_id}"
                            translated_synopsis, reliable = translator.translate(text=src_synopsis)
                            if reliable:
                                self.pending_films[film_id][PENDING_TO_TRANSLATE][target_lang][
                                    SYNOPSIS] = translated_synopsis
                            else:
                                logger.warning(
                                    f"Translation of {film_id} was not reliable. Not adding it to the database")