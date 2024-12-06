from __future__ import annotations

import os

from requests import ReadTimeout

from nlp.language_detection import LanguageDetector
from scrapers.BaseScraper import BaseScraper
import requests
from slugify import slugify

from scrapers.constants.FilmAffinity_films_inspector import TECHNICAL_INFO_XPATH, ORIGINAL_TITLE_XPATH, \
    OTHER_TITLES_XPATH, DATE_XPATH, DURATION_XPATH, COUNTRY_XPATH, EACH_GENRE_XPATH, EACH_TOPIC_XPATH, \
    EACH_DIRECTOR_GRANDPARENT_XPATH, DIRECTORS_WRAPPER_XPATH, DIRECTOR_XPATH, DIRECTOR_MORE_INFO_XPATH, \
    SCREEN_WRITERS_TITLE, GET_TECHNICAL_STAFF_WRAPPER_XPATH, EACH_STAFF_PARENT_XPATH, MUSICIANS_TITLE, \
    CINEMATOGRAPHERS_TITLE, EACH_STAFF_XPATH_DICT, CAST_TITLE, GET_INVALID_STAFF_XPATH, \
    ACCEPTABLE_INVALID_STAFF, EACH_STAFF_ROLE_PARENT_SIBLING_XPATH, PRODUCERS_TITLE, COUNTRIES_CO_PRODUCTION_XPATH, \
    COUNTRIES_CO_PRODUCTION_START_STR, COUNTRIES_CO_PRODUCTION_SEPARATOR, EACH_STAFF_ROLE_XPATH, MOVIE_SAGA, \
    MOVIE_SAGA_XPATH, SYNOPSIS_XPATH, AWARDS_WRAPPER_XPATH, EACH_AWARD_YEAR_XPATH, \
    EACH_AWARD_TEXT_XPATH, RATING_WRAPPER_XPATH, RATING_XPATH, RATING_VOTES_XPATH, REVIEWS_COUNT_XPATH, \
    RELEVANT_LINKS_XPATH, AVAILABLE_AT_WRAPPER_XPATH, JUST_WATCH_URL_XPATH, AVAILABLE_AT_WRAPPER_BODY_XPATH, \
    FLATRATE_PLATFORMS_WRAPPER_XPATH, BUY_PLATFORMS_WRAPPER_XPATH, EACH_AVAILABLE_AT_XPATH, \
    EACH_AVAILABLE_AT_PLATFORM_DESCRIPTION_XPATH, PLATFORM_XPATH_BY_TYPE, LANG_TITLE_XPATH, POSTER_XPATH, \
    GET_CAST_WRAPPER_XPATH, EACH_ACTOR_PARENT_XPATH_ON_CARDS, YOUTUBE_ID_REGEX
from scrapers.constants.FilmAffinity_link_discovering import MOVIE_CARD_XPATH, MOVIE_ID_ATTRIB, \
    MOVIE_TITLE_ATTRIB_XPATH, \
    MOVIE_TITLE_ATTRIB, MOVIE_URL_ATTRIB, AMOUNT_OF_PAGES_ADV_SEARCH_XPATH, CURRENT_AND_MAX_PAGES_XPATH
from scrapers.constants.FilmAffinity import URL, TITLE, COUNTRY, YEAR, ORIGINAL_TITLE, CHARACTERS_TO_REMOVE_FROM_BOUNDS, \
    OTHER_TITLES, DURATION_MINUTES, GENRES, TOPICS, STAFF, VALID_DIRECTORS_MORE_INFO, NAME, ROLE, DIRECTORS, \
    SCREENWRITERS, MUSICIANS, CINEMATOGRAPHERS, CAST, VALID_STAFF_MORE_INFO, DELETE_ENTRY_MARK, InvalidMovieException, \
    PRODUCERS, BASIC_INFO, COUNTRIES, TOPICS_TO_DELETE, FILM_AFFINITY_INFO, ID, SYNOPSIS, EXTENDED_INFO, NOMINATIONS, \
    TEXT, \
    KNOWN_AWARDS, TO, AWARD, SCORE, AVERAGE_SCORE, VOTES, REVIEWS_COUNT, RELEVANT_LINKS, RELEVANT_LINKS_URL_TO_SITE, \
    AVAILABLE_AT, JUST_WATCH, AVAILABLE_AT_PLATFORMS_TO_AVOID, AVAILABLE_AT_DELETE_PARAMS_PLATFORMS, \
    LANGUAGES, KNOWN_TITLE_PARENTHESIS_TO_DELETE, FILM_AFFINITY_WEB_LANGS, \
    REGEX_TO_DELETE_FROM_SYNOPSIS, POSTER_URL, PENDING_TO_TRANSLATE, RELEVANT_LINKS_TO_AVOID, KNOWN_AWARDS_LOWERCASE, \
    SLUG, FILM_AFFINITY_SYNOPSIS, ALTERNATIVE_MULTIMEDIA, JUST_WATCH_SYNOPSIS, TRAILER_URL, EXTRA_CAST_KEYS, \
    JUST_WATCH_LINKS_TO_AVOID, AVAILABLE_AT_PLATFORM_MONETIZATION, AVAILABLE_AT_PLATFORM, AVAILABLE_AT_PLATFORMS, \
    ORIGINAL_LANGS, PUBLICATION_DATE

import re
from loguru import logger
from lxml.html import HtmlElement
import ftfy
from lxml.etree import _ElementUnicodeResult

from nlp.config import SOURCE_LANG_FROM_TARGET
from nlp.languages import ENGLISH, SPANISH
from nlp.translator import Translator
import spacy
import json

from scrapers.constants.base import JUST_WATCH_WORD_TRANSLATIONS

NER_MODELS = {
    SPANISH: spacy.load("es_dep_news_trf", disable=["tagger", "parser", "attribute_ruler", "lemmatizer"],),
    ENGLISH: spacy.load("en_core_web_trf", disable=["tagger", "parser", "attribute_ruler", "lemmatizer"])
}

BASE_SCRAPER = BaseScraper()
LANGUAGE_DETECTOR = LanguageDetector()
with open(os.path.join('resources', 'FilmAffinity', 'countries_to_lang.json')) as f:
    COUNTRIES_TO_LANG = json.load(f)


def extract_movies_from_page(html: HtmlElement, year: int, country: str) -> dict[str, dict[str, str]]:
    films = {}
    current_movie_cards = html.xpath(MOVIE_CARD_XPATH)
    assert len(current_movie_cards) > 0, "No movie cards found"
    for movie_card in current_movie_cards:
        # Get the data-movie-id attribute
        movie_id = movie_card.attrib[MOVIE_ID_ATTRIB]
        assert movie_id not in films, f"Movie {movie_id} already in the list"
        # Get the film title
        title_element = movie_card.xpath(MOVIE_TITLE_ATTRIB_XPATH)
        assert len(title_element) == 1, f"Expected 1 title element, got {len(title_element)}"
        title_element = title_element[0]
        # Get the title
        title = clean_name(name=title_element.attrib[MOVIE_TITLE_ATTRIB], reencode=True)
        # Get the url
        url = title_element.attrib[MOVIE_URL_ATTRIB]
        films[movie_id] = {
            TITLE: title,
            URL: url,
            YEAR: year,
            COUNTRY: country
        }
    return films


def extract_info_from_movie_page(html: HtmlElement, countries_inverse_dict: dict[str, str],
                                 genres_inverse_dict: dict[str, str], card_info: dict[str, str] | None = None) -> dict[
    str, dict]:
    """
    Extract the information of the movie page
    :param html: HtmlElement. The html of the page
    :param countries_inverse_dict: dict[str, str]. The dictionary with the countries as key and the country code as value
    :param genres_inverse_dict: dict[str, str]. The dictionary with the genres as key and the genre code as value
    :param card_info: dict[str, str]. The information of the card of the movie. If given, used just for
    sanity checking.
    :return: dict. The information of the movie
    """
    movie_info = {}
    # Get the title
    technical_info_section = html.xpath(TECHNICAL_INFO_XPATH)
    assert len(technical_info_section) == 1, f"Expected 1 movie info section, got {len(technical_info_section)}"
    technical_info_section = technical_info_section[0]

    # ----------- GET THE BASIC TECHNICAL INFO -------------
    movie_info[BASIC_INFO] = get_basic_technical_info(technical_info_section=technical_info_section,
                                                      countries_inverse_dict=countries_inverse_dict,
                                                      genres_inverse_dict=genres_inverse_dict, card_info=card_info)
    movie_info[SLUG] = slugify(movie_info[BASIC_INFO][ORIGINAL_TITLE])

    movie_info[STAFF] = get_staff_info(technical_info_section=technical_info_section)

    movie_info[EXTENDED_INFO] = get_extended_info(html=html, staff=movie_info[STAFF])

    movie_info[FILM_AFFINITY_INFO] = get_film_affinity_info(html=html,
                                                            card_info=card_info)
    movie_info[AVAILABLE_AT], movie_info[ALTERNATIVE_MULTIMEDIA] = get_just_watch_info(html=html)
    movie_info[BASIC_INFO][PUBLICATION_DATE] = movie_info[ALTERNATIVE_MULTIMEDIA].pop(PUBLICATION_DATE, None)

    improved_cast = movie_info[ALTERNATIVE_MULTIMEDIA].get(CAST, [])
    if len(improved_cast) > 0:
        # For each new actor found
        for actor in improved_cast:
            # Iterate over each already known actor (from FilmAffinity)
            for i, already_known_actor in enumerate(movie_info[STAFF].get(CAST, [])):
                # If it did exist but had no role, update the role to the new one found
                if actor[NAME].lower() == already_known_actor[NAME].lower() and already_known_actor[ROLE] is None and actor[ROLE] is not None:
                    role = re.sub(r'\s*\(.*?\)\s*', ' ', actor[ROLE]).strip()
                    movie_info[STAFF][CAST][i][ROLE] = role
                    break
            # If it didn't existed, add it
            else:
                movie_info[STAFF][CAST].append(actor)

        movie_info[ALTERNATIVE_MULTIMEDIA].pop(CAST)


    original_languages = get_film_affinity_basic_languages(html=html, url=card_info[URL], current_movie_info=movie_info,
                                                           movie_languages_info={})
    movie_info[FILM_AFFINITY_SYNOPSIS] = original_languages
    #movie_info[LANGUAGES] = translate_to_all_available_languages(original_languages=original_languages,
    #                                                             original_title=movie_info[BASIC_INFO][ORIGINAL_TITLE])

    return movie_info


def get_basic_technical_info(technical_info_section: HtmlElement, countries_inverse_dict: dict[str, str],
                             genres_inverse_dict: dict[str, str],
                             card_info: dict[str, str] | None = None) -> dict[str, str]:
    movie_info = {}

    # Get the title
    title_element = technical_info_section.xpath(ORIGINAL_TITLE_XPATH)
    assert len(title_element) == 1, f"Expected 1 title element, got {len(title_element)}"
    movie_info[ORIGINAL_TITLE] = clean_name(name=title_element[0].text, reencode=True)

    # Get the other titles
    other_titles = technical_info_section.xpath(OTHER_TITLES_XPATH)
    movie_info[OTHER_TITLES] = [clean_name(name=title.text, reencode=True) for title in other_titles]


    # Get the year
    year = technical_info_section.xpath(DATE_XPATH)
    assert len(year) == 1, f"Expected 1 year element, got {len(year)}"
    year = clean_name(name=year[0].text)
    assert year.isdigit(), f"Expected year to be a number, got {year}"
    if card_info is not None:
        # Sanity check
        pass
        # assert int(year) == int(card_info[YEAR]), f"Expected year {card_info[YEAR]}, got {year}"
    movie_info[YEAR] = int(year)

    # Get the duration
    duration = technical_info_section.xpath(DURATION_XPATH)
    if len(duration) == 0:
        # No duration found
        movie_info[DURATION_MINUTES] = None
    else:
        assert len(duration) == 1, f"Expected 1 duration element, got {len(duration)}"
        movie_info[DURATION_MINUTES] = clean_duration(duration=duration[0].text)

    # Get the country
    country = technical_info_section.xpath(COUNTRY_XPATH)
    assert len(country) == 1, f"Expected 1 country element, got {len(country)}"
    country = country[0]
    assert country in countries_inverse_dict, f"Country {country} not in the countries dictionary"
    original_country = countries_inverse_dict[country]
    other_countries = find_countries_co_production(technical_info_section=technical_info_section,
                                                   countries_dictionary=countries_inverse_dict)
    movie_info[COUNTRIES] = [original_country] if len(other_countries) == 0 else other_countries
    original_langs = []
    for country in movie_info[COUNTRIES]:
        original_langs.extend(COUNTRIES_TO_LANG.get(country, []))

    movie_info[ORIGINAL_LANGS] = list(set(original_langs))


    if card_info is not None:
        # Sanity check
        # assert any(country == card_info[COUNTRY] for country in movie_info[COUNTRIES]), f"Expected country {card_info[COUNTRY]}, got {movie_info[COUNTRY]}"
        pass
    # Get the genres
    genres = technical_info_section.xpath(EACH_GENRE_XPATH)
    assert len(genres) > 0, f"Expected at least 1 genre, got {len(genres)}"
    assert all(genre.text in genres_inverse_dict for genre in genres), f"Genres {genres} not in the genres dictionary"
    movie_info[GENRES] = [genres_inverse_dict[genre.text] for genre in genres]

    # Get the topics
    topics = technical_info_section.xpath(EACH_TOPIC_XPATH)
    assert not any(topic.text in genres_inverse_dict for topic in topics), f"Topics {topics} in the genres dictionary"
    movie_info[TOPICS] = [clean_name(name=topic.text, reencode=True) for topic in topics]
    if any(topic in TOPICS_TO_DELETE for topic in movie_info[TOPICS]):
        raise InvalidMovieException("Movie has an invalid topic: " + str(movie_info[TOPICS]))

    # Get the saga to which the movie belongs
    movie_saga = technical_info_section.xpath(MOVIE_SAGA_XPATH)
    saga = clean_name(name=movie_saga[0].text, reencode=True) if len(movie_saga) == 1 else None
    assert saga is None or saga != "", "Movie saga is empty"
    movie_info[MOVIE_SAGA] = saga

    return movie_info


def get_extended_info(html: HtmlElement, staff: dict[str, list[dict[str, str]]]) -> dict[str, list[dict[str, str]]]:
    movie_info = {}

    # Get the awards
    movie_info[NOMINATIONS] = get_film_awards(html=html, staff=staff)

    # Get the relevant links
    relevant_links = get_relevant_links(html)
    movie_info[RELEVANT_LINKS] = relevant_links

    # Get the poster_url
    poster_url = html.xpath(POSTER_XPATH)
    if len(poster_url) < 1:
        raise InvalidMovieException(f"Expected 1 poster image url, got {len(poster_url)}")
    poster_url = poster_url[0].get("src")
    if poster_url == "#":
        poster_url = None
    movie_info[POSTER_URL] = poster_url
    if 'noimgfull' in poster_url:
        raise InvalidMovieException(f"Film has no poster. Skipping it")


    return movie_info


def get_film_affinity_basic_languages(html: HtmlElement, url: str, current_movie_info: dict[
    str, str | int | list[str] | dict[dict[str, str | None]]],
                                      movie_languages_info: dict[str, dict[str, str]]) -> dict[dict[str, str | None]]:
    """
    Get the languages_info. Receives movie_info as a parameter for allowing recursive behaviour
    """
    # Get position the lang in the url (url: https://www.filmaffinity.com/lang_code/film123456.html)
    lang = re.findall(fr"\/({'|'.join(FILM_AFFINITY_WEB_LANGS)})\/", url)
    assert len(lang) == 1, f"Expected 1 language in the url, got {len(lang)}"
    lang = lang[0]
    assert lang not in movie_languages_info, f"Language {lang} already in the movie info"
    lang_title = html.xpath(LANG_TITLE_XPATH)
    assert len(lang_title) == 1, f"Expected 1 language title, got {len(lang_title)}"
    lang_title = clean_movie_title(title=lang_title[0].text)

    technical_info = html.xpath(TECHNICAL_INFO_XPATH)
    assert len(technical_info) == 1, f"Expected 1 technical info section, got {len(technical_info)}"
    technical_info = technical_info[0]
    cast = tuple(person[NAME] for person in  current_movie_info[STAFF][CAST])
    synopsis = get_synopsis(technical_info=technical_info, cast=cast, lang=lang)
    if synopsis is None:
        raise InvalidMovieException(f"No synopsis retrieved for movie: {current_movie_info[BASIC_INFO][ORIGINAL_TITLE]} in language: {lang}")
    if "filmaffinity" in synopsis.lower() or "film affinity" in synopsis.lower():
        raise InvalidMovieException(f"Film Affinity Mark detected in synopsis: {synopsis}")

    movie_languages_info[lang] = {TITLE: lang_title, SYNOPSIS: synopsis}

    non_inspected_langs = tuple(lang for lang in FILM_AFFINITY_WEB_LANGS if lang not in movie_languages_info)
    if len(non_inspected_langs) > 0:
        new_url = url.replace(lang, non_inspected_langs[0])
        new_html = BASE_SCRAPER.get(url=new_url)
        # Recursive call
        movie_languages_info = get_film_affinity_basic_languages(html=new_html, url=new_url,
                                                                 current_movie_info=current_movie_info,
                                                                 movie_languages_info=movie_languages_info)
    assert all(lang in movie_languages_info for lang in (SPANISH, ENGLISH)), f"Expected languages {SPANISH} and " \
                                                                             f"{ENGLISH}, got {tuple(movie_languages_info.keys())}"
    return movie_languages_info


def get_translated_titles_film_affinity_languages(original_languages: dict[dict[str, str | None]]) -> dict[
    str, str | None]:
    assert all(lang in (ENGLISH, SPANISH) for lang in
               original_languages), f"Expected only English and Spanish, got {original_languages}"
    lang_titles = {}
    for lang, lang_info in original_languages.items():
        assert lang_info[TITLE] is not None, f"Title is None for language {lang}"
        detected_lang = LANGUAGE_DETECTOR.detect_lang(text=lang_info[TITLE])
        lang_titles[lang] = lang_info[TITLE] if detected_lang == lang else None
    # If there is only one title in the original language, translate the other ones
    available_translations = tuple(lang for lang, title in lang_titles.items() if title is not None)
    if len(available_translations) == 1:
        source_lang, target_lang = (ENGLISH, SPANISH) if available_translations[0] == ENGLISH else (SPANISH, ENGLISH)
        with Translator(lang_pair=(source_lang, target_lang)) as translator:
            title, reliable = translator.translate(text=lang_titles[source_lang])
            lang_titles[target_lang] = title if reliable else None
    return lang_titles


def get_relevant_links(html: HtmlElement) -> list[dict[str, str]]:
    """
    Get the relevant links of the movie
    :param html: The html of the filmAffinity movie page

    :return: A list of dictionaries with the relevant links
    """
    relevant_links_wrapper = html.xpath(RELEVANT_LINKS_XPATH)
    relevant_links = []
    for link in relevant_links_wrapper:
        href = link.get("href")
        assert href not in (None, ""), f"Expected href not to be empty, got {href}"
        site = None
        for site_url, site_data in RELEVANT_LINKS_URL_TO_SITE.items():
            if site_url in href:
                assert site is None, f"Expected only one site to match, got {site} and {site_data}"
                site = site_data
        if site is None:
            logger.warning(f"Could not find a site for the link {href}")
            continue
        relevant_links.append({URL: href, **site})
    return relevant_links


def get_film_awards(html: HtmlElement, staff: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    awards_wrapper = html.xpath(AWARDS_WRAPPER_XPATH)
    if len(awards_wrapper) == 0:
        return []
    else:
        assert len(awards_wrapper) == 1, f"Expected 1 awards wrapper, got {len(awards_wrapper)}"
        awards_wrapper = awards_wrapper[0]
        awards = awards_wrapper.xpath(EACH_AWARD_YEAR_XPATH)
        if len(awards) == 0:
            logger.warning("No awards found within the section. Likely because of a format error")
            return []
        staff_names = tuple(set([person[NAME] for persons in staff.values() for person in persons]))
        awards_list = []
        for award in awards:
            award_year = clean_name(name=award.text)
            assert award_year.isdigit(), f"Expected award year to be a number, got {award_year}"
            award_text = award.xpath(EACH_AWARD_TEXT_XPATH)
            assert len(award_text) == 1, f"Expected 1 award text, got {len(award_text)}"
            award_text = clean_name(name=award_text[0], reencode=True)
            award_type = award_text.split(':')
            if len(award_type) == 1:
                award_type = award_text.split(',')
            award_type = award_type[0]
            know_award = [known_award for known_award in KNOWN_AWARDS_LOWERCASE if known_award in award_type.lower()]
            assert len(know_award) > 0, f"Expected a known award (award type: {award_type})"
            know_award = KNOWN_AWARDS_LOWERCASE[know_award[0]]
            # Get all the texts that are between parentheses
            possible_receivers = [receiver for receiver in re.findall(r'\((.*?)\)', award_text) if
                                  any(receiver.lower() in staff_name.lower() for staff_name in staff_names)]
            if len(possible_receivers) == 0:
                receiver = [None]
            else:
                receiver = [staff_name for staff_name in staff_names if
                            any(receiver.lower() in staff_name.lower() for receiver in possible_receivers)]
                if len(receiver) != len(possible_receivers):
                    logger.warning(f"Expected {len(possible_receivers)} receivers, got {len(receiver)} ({receiver}), not assigning to anyone")
                    receiver = [None]
            awards_list.extend(
                [{YEAR: int(award_year), AWARD: know_award, TEXT: award_text, TO: to} for to in receiver])
        # Sort the list by year and then by name
        awards_list.sort(key=lambda award: (award[YEAR], award[AWARD]))
        return awards_list


def get_staff_info(technical_info_section: HtmlElement) -> dict[str, list[str | dict[str, str]]]:
    movie_info = {}

    # Get the directors
    movie_info[DIRECTORS] = get_directors(technical_info_section=technical_info_section)
    movie_info[SCREENWRITERS] = get_staff(technical_info_section=technical_info_section,
                                          staff_type=SCREEN_WRITERS_TITLE, accept_empty=True)
    movie_info[MUSICIANS] = get_staff(technical_info_section=technical_info_section,
                                      staff_type=MUSICIANS_TITLE, accept_empty=True)
    movie_info[CINEMATOGRAPHERS] = get_staff(technical_info_section=technical_info_section,
                                             staff_type=CINEMATOGRAPHERS_TITLE, accept_empty=True)
    movie_info[CAST] = get_staff(technical_info_section=technical_info_section,
                                 staff_type=CAST_TITLE, accept_empty=True)
    movie_info[PRODUCERS] = get_staff(technical_info_section=technical_info_section, staff_type=PRODUCERS_TITLE,
                                      accept_empty=True)

    return movie_info


def get_film_affinity_info(html: HtmlElement, card_info: dict[str, str]) -> dict[
    str, str]:
    """
    Get the FilmAffinity info
    :param html: The HTML of the movie page
    :param technical_info_section: The technical info section
    :param card_info: The card info from the inspector
    """
    movie_info = {}

    # Get the FilmAffinity URL
    movie_info[URL] = card_info[URL]

    # Get the rating
    movie_info[SCORE] = get_score_info(html=html)

    return movie_info


def get_synopsis(technical_info: HtmlElement, lang: str, cast: tuple[str] = ()) -> str | None:
    synopsis = technical_info.xpath(SYNOPSIS_XPATH)
    if len(synopsis) == 0 or synopsis[0] is None:
        return None
    else:
        assert len(synopsis) == 1, f"Expected 1 synopsis, got {len(synopsis)}"
        synopsis = clean_synopsis(synopsis=synopsis[0].text, lang=lang, cast = cast)
        if synopsis == "":
            logger.warning("The synopsis became empty after cleaning")
            synopsis = None
        return synopsis


def get_score_info(html: HtmlElement) -> dict[str, float | int | None]:
    """
    Get the score info
    :param html: The HTML of the movie page
    """
    rating_wrapper = html.xpath(RATING_WRAPPER_XPATH)
    if rating_wrapper == []:
        return {AVERAGE_SCORE: None, VOTES: None, REVIEWS_COUNT: None}
    else:
        assert len(rating_wrapper) == 1, f"Expected 1 rating wrapper, got {len(rating_wrapper)}"
        rating_wrapper = rating_wrapper[0]
        rating = rating_wrapper.xpath(RATING_XPATH)
        assert len(rating) == 1, f"Expected 1 rating, got {len(rating)}"
        rating = clean_name(name=rating[0], reencode=True)

        # Get the number of votes
        votes = rating_wrapper.xpath(RATING_VOTES_XPATH)
        assert len(votes) == 1, f"Expected 1 rating votes, got {len(votes)}"
        votes = clean_name(name=votes[0], reencode=True)
        assert votes.isdigit(), f"Expected the number of votes to be a number, got {votes}"

        # Get the number of reviews
        reviews = rating_wrapper.xpath(REVIEWS_COUNT_XPATH)
        assert len(reviews) == 1, f"Expected 1 review count, got {len(reviews)}"
        reviews = clean_name(name=reviews[0], reencode=True)
        assert reviews.isdigit(), f"Expected the number of reviews to be a number, got {reviews}"
        return {AVERAGE_SCORE: float(rating), VOTES: int(votes), REVIEWS_COUNT: int(reviews)}


def get_just_watch_info(html: HtmlElement) -> tuple[dict[str, list[dict[str, str] | None]], dict[str, str | None]]:
    """
    Get the information about all the platforms where the movie is available
    :param html: The HTML of the movie page
    """
    available_at_info = {}
    wrapper = html.xpath(AVAILABLE_AT_WRAPPER_XPATH)
    just_watch_url, available_sites = None, []
    just_watch_multimedia = {}
    if len(wrapper) > 0:
        assert len(wrapper) == 1, f"Expected 1 wrapper, got {len(wrapper)}"
        wrapper = wrapper[0]
        just_watch = wrapper.xpath(JUST_WATCH_URL_XPATH)
        if len(just_watch) > 0:
            assert len(just_watch) == 1, f"Expected 1 JustWatch URL, got {len(just_watch)}"
            just_watch_url = just_watch[0].get("href")
            if not just_watch_url.endswith('justwatch.com'):

                assert just_watch_url not in (None, ""), "JustWatch URL is empty"
                response, just_watch_url = BASE_SCRAPER.get(url=just_watch_url, return_url=True)
                try:
                    ld_json = response.head.xpath('script[@type="application/ld+json"]/text()')
                    ld_json = json.loads(ld_json[0])
                except AttributeError:
                    logger.error("We got probably temporally blocked by JustWatch")
                    raise ReadTimeout
                publication_date = ld_json['dateCreated']
                available_at_info[JUST_WATCH] = just_watch_url if response is not None else None
                body = response.xpath('./body')
                assert len(body) == 1, f"Body not found in JustWatch. Found {len(body)}"
                body = body[0]
                just_watch_multimedia = get_just_watch_multimedia(html=body)
                just_watch_multimedia[POSTER_URL] = ld_json['image']
                just_watch_multimedia[PUBLICATION_DATE] = publication_date
                if 'aggregateRating' in ld_json and 'ratingValue' in ld_json['aggregateRating']:
                    just_watch_multimedia[SCORE] = float(ld_json['aggregateRating']['ratingValue'])/10
                else:
                    logger.warning("No rating in justwatch film")
                streaming_row_wrapper = body.xpath("//div[contains(@class, 'buybox-row stream')]")
                if len(streaming_row_wrapper) == 1:
                    streaming_row_wrapper = streaming_row_wrapper[0]
                    site_as = streaming_row_wrapper.xpath("//div[contains(@class, 'buybox-row stream')]//a")
                    for site in site_as:
                        platform = site.xpath(".//img")[0].get('alt')
                        offer_label = str(site.xpath("./div[contains(@class, 'offer__label')]/span/text()")[0])
                        href = site.get('href')
                        if href is None or any(link.lower() in href.lower() for link in JUST_WATCH_LINKS_TO_AVOID):
                            continue

                        # Delete the params (usually refs) from href
                        platform_html, href = BASE_SCRAPER.get(url=href, return_url=True)

                        href = href.split('?')[0]
                        if href is None or any(link.lower() in href.lower() for link in JUST_WATCH_LINKS_TO_AVOID):
                            continue

                        offer_label = JUST_WATCH_WORD_TRANSLATIONS.get(offer_label, None)
                        if offer_label is None:
                            continue
                        available_sites.append({
                            AVAILABLE_AT_PLATFORM: platform,
                            AVAILABLE_AT_PLATFORM_MONETIZATION: offer_label,
                            URL: href
                        })

                else:
                    logger.warning("No streaming row found in JustWatch")

    available_at_info = {JUST_WATCH: just_watch_url,
                         AVAILABLE_AT_PLATFORMS: available_sites}

    return available_at_info, just_watch_multimedia

def get_just_watch_multimedia(html):
    synopsis = html.xpath("//div[h2[contains(., 'Synopsis')]]/following-sibling::p/text()")
    synopsis = clean_synopsis(synopsis=synopsis[0], lang=ENGLISH) if len(synopsis) == 1 else None

    poster = None
    trailer_url = None

    youtube_miniature = html.xpath("//div[contains(@class, 'youtube-player')]/img[contains(@alt, 'Trailer Preview Image')]")
    if len(youtube_miniature) == 1:
        miniature_url = youtube_miniature[0].get('data-src')
        matches = re.findall(YOUTUBE_ID_REGEX, miniature_url)
        if len(matches) == 1:
            trailer_url = f"https://www.youtube.com/watch?v={matches[0]}"

    # Finally take the cast correspondant
    cast = []
    cast_wrapper = html.xpath("//h3[contains(text(), 'Cast')]/../following-sibling::div[1]")
    if len(cast_wrapper) > 0:
        cast_wrapper = cast_wrapper[0]
        actors = cast_wrapper.xpath(".//div[contains(@class, 'title-credits__actor')]")
        for actor in actors:
            # Extract the name of the actor
            name = actor.xpath(".//span[contains(@class, 'title-credit-name')]/text()")
            if len(name) != 1:
                continue
            name = name[0]
            # Extract the role of the actor
            role = actor.xpath(".//div[contains(@class, 'title-credits__actor--role--name')]/strong/@title")
            if len(role) == 0:
                role = None
            else:
                role = role[0]
                if any(extra_keyword.lower() in role.lower() for extra_keyword in EXTRA_CAST_KEYS):
                    continue
            cast.append({
                NAME: clean_name(name=name),
                ROLE: clean_name(name=role) if role is not None else None
            })

    alternative_info = {
        POSTER_URL: poster,
        JUST_WATCH_SYNOPSIS: synopsis,
        TRAILER_URL: trailer_url,
        CAST: cast
    }

    return alternative_info


def get_staff(technical_info_section: HtmlElement, staff_type: str, accept_empty: bool = False) -> list[
    str | dict[str, str]]:
    wrapper_xpath = GET_TECHNICAL_STAFF_WRAPPER_XPATH(title=staff_type) if staff_type.lower() != "cast" else GET_CAST_WRAPPER_XPATH
    staff = technical_info_section.xpath(wrapper_xpath)
    if len(staff) == 0:
        if not accept_empty:
            invalid_staff = technical_info_section.xpath(GET_INVALID_STAFF_XPATH(title=staff_type))
            assert len(invalid_staff) > 0, f"Expected at least 1 invalid {staff_type}, got {len(invalid_staff)}"
            invalid_staff_names = [clean_name(name=staff.text, reencode=True) for staff in invalid_staff]
            if len(invalid_staff_names) == 1:
                # Sometimes they just appear as a single string separated by commas
                invalid_staff_names = [invalid_name.strip() for invalid_name in invalid_staff_names[0].split(",")]
            assert all(invalid_name in ACCEPTABLE_INVALID_STAFF[staff_type] for invalid_name in invalid_staff_names), \
                f"Invalid staff {[clean_name(name=invalid.text) for invalid in invalid_staff]} not in the acceptable invalid staff dictionary"

        return []
    assert len(staff) == 1, f"Expected 1 {staff_type} element, got {len(staff)}"
    staff = staff[0]
    is_final = False
    if staff_type.lower() == 'cast':
        # Try with the new cards they are implementing
        cast = staff.xpath(EACH_ACTOR_PARENT_XPATH_ON_CARDS)
        if len(cast) == 0:
            cast = staff.xpath(EACH_STAFF_PARENT_XPATH)
        else:
            roles = [[] for person in cast]
            is_final = True
        staff = cast
    else:
        staff = staff.xpath(EACH_STAFF_PARENT_XPATH)
        assert len(staff) > 0, f"Expected at least 1 {staff_type}, got {len(staff)}"
        each_staff_xpath = EACH_STAFF_XPATH_DICT[staff_type]
        staff = [person.xpath(each_staff_xpath) for person in staff]

        if not all(len(person) == 1 for person in staff):
            logger.warning(f"Expected 1 {staff_type} element, got {staff}")
            return []

    if not is_final:
        staff = [person[0] for person in staff]
        roles_xpath = EACH_STAFF_ROLE_XPATH[staff_type]
        roles = [person.xpath(roles_xpath) for person in staff] if roles_xpath is not None else []
        if staff_type.lower() == 'cast' and len(staff) > 0 and any(person.text is None for person in staff):
            staff = [person.xpath('./span')[0] for person in staff]

    assert all(len(role) <= 1 for role in roles), f"Expected at most 1 {staff_type} role, got {roles}"
    roles_list, last_role = [], None
    for role in roles:
        if len(role) == 1:
            last_role = role = VALID_STAFF_MORE_INFO[clean_name(name=role[0].text)]
        else:
            role = last_role
        roles_list.append(role)

    staff = [clean_name(name=person.text, reencode=True) for person in staff]
    assert all(person != "" for person in staff), f"Expected all {staff_type} to be non-empty, got {staff}"
    assert len(staff) == len(roles_list), f"Expected {len(staff)} {staff_type} roles, got {len(roles_list)}"
    staff_roles = {}
    for person, role in zip(staff, roles_list):
        if person in staff_roles:
            if staff_roles[person] not in (None, role):
                logger.warning(f"Expected {person} to have no previous role or have the same one when appearing twice, got {staff_roles[person]}")
                continue
            if role is None:
                logger.warning(f"Expected {person} to have a role when appearing twice as a {staff_type}, got None")
        staff_roles[person] = role
        if role == DELETE_ENTRY_MARK:
            raise InvalidMovieException(f"Invalid {staff_type} {person}")
    staff = [{NAME: person, ROLE: role} for person, role in staff_roles.items()]
    return staff


def get_directors(technical_info_section: HtmlElement) -> list[dict[str, str]]:
    directors_wrapper = technical_info_section.xpath(DIRECTORS_WRAPPER_XPATH)
    if len(directors_wrapper) == 0:
        logger.warning("No directors found")
        return []
    assert len(directors_wrapper) == 1, f"Expected 1 directors wrapper, got {len(directors_wrapper)}"
    directors_wrapper = directors_wrapper[0]
    directors = directors_wrapper.xpath(EACH_DIRECTOR_GRANDPARENT_XPATH)
    directors_dict = {}
    for director_html in directors:
        director = director_html.xpath(DIRECTOR_XPATH)
        assert len(director) == 1, f"Expected 1 director element, got {len(director)}"
        director = clean_name(name=director[0].text, reencode=True)
        if director in directors_dict:
            continue
        more_info = director_html.xpath(DIRECTOR_MORE_INFO_XPATH)
        assert len(more_info) <= 1, f"Expected at most 1 more info element, got {len(more_info)}"
        if len(more_info) == 1:
            more_info = more_info[0].text
            assert more_info in VALID_DIRECTORS_MORE_INFO, f"Expected more info to be in {VALID_DIRECTORS_MORE_INFO}, got {more_info}"
            more_info = VALID_DIRECTORS_MORE_INFO[more_info]
        else:
            more_info = None
        directors_dict[director] = more_info
    directors = [{NAME: director, ROLE: more_info} for director, more_info in directors_dict.items()]

    return directors


def find_countries_co_production(technical_info_section: HtmlElement, countries_dictionary: dict[str, str]) -> list[
    str]:
    """
    There are some cases where the producers do just say something like co-production Italy-Spain

    :param technical_info_section: HtmlElement. The wrapper containing all the technical info
    :return: list[HtmlElement]. The list of the producers
    """
    co_production = technical_info_section.xpath(COUNTRIES_CO_PRODUCTION_XPATH)
    if len(co_production) == 0:
        return []
    assert len(co_production) == 1, f"Expected 1 co-production element, got {len(co_production)}"
    co_production = clean_name(name=co_production[0].text, reencode=True)
    if not co_production.startswith(COUNTRIES_CO_PRODUCTION_START_STR):
        return []
    co_production = co_production[len(COUNTRIES_CO_PRODUCTION_START_STR):].strip()
    co_production_orig = co_production.split(COUNTRIES_CO_PRODUCTION_SEPARATOR)
    co_production = [country.strip() for country in co_production_orig if country.strip() in countries_dictionary]
    if len(co_production) < len(co_production_orig):
        logger.warning(f"Expected all countries in {co_production_orig} to be in the countries dictionary, got {co_production}")
    logger.info(f"Found co-production countries: {co_production}")
    co_production = [countries_dictionary[country] for country in co_production]
    return co_production


def clean_duration(duration: str) -> int:
    """
    Clean the duration of the movie
    :param duration: str. The duration of the movie
    :return: int. The duration of the movie in minutes
    """
    assert duration.endswith("min."), f"Expected duration to end with 'min', got {duration}"
    duration = clean_name(name=duration.replace(" min.", ""))
    assert duration.isdigit(), f"Expected duration to be a number, got {duration}"
    return int(duration)


def get_max_pages(html: HtmlElement, current_page: int = 1) -> int | None:
    """
    Get the maximum number of pages, given the "Page 1 of X" text of the website
    :param html: HtmlElement. The html of the page
    :param current_page: int. The current page. Just used for sanity checking
    :return: int or None. The maximum number of pages of the search. None if there is no pagination (no films case)
    """
    amount_of_pages = html.xpath(AMOUNT_OF_PAGES_ADV_SEARCH_XPATH)
    assert len(amount_of_pages) <= 1, f"Expected 0 or 1 amount of pages, got {len(amount_of_pages)}"
    if len(amount_of_pages) == 0:
        return None
    amount_of_pages = amount_of_pages[0].xpath(CURRENT_AND_MAX_PAGES_XPATH)
    assert len(amount_of_pages) == 0 or len(
        amount_of_pages) == 2, f"Expected 0 (single page) or 2 (current, max_pages) " \
                               f"pages identifiers, got {len(amount_of_pages)}"
    if len(amount_of_pages) == 0:
        assert current_page == 1, f"Expected current page to be 1, got {current_page}"
        return 1
    current, max_pages = [int(page.text) for page in amount_of_pages]
    assert current == current_page, f"Expected current page to be {current_page}, got {current}"
    return max_pages


def clean_name(name: str | _ElementUnicodeResult, reencode: bool = False) -> str:
    """
    Clean the name of the movie, removing all kind of characters like /n, /t, etc
    :param name: str. The name of the movie
    :param reencode: bool. If True, reencode the name to utf-8
    :return: str. The cleaned name
    """
    assert type(name) in (str, _ElementUnicodeResult), f"Expected name to be a string, got {type(name)}"
    keep_looking = True
    while keep_looking:
        keep_looking = False
        for char in CHARACTERS_TO_REMOVE_FROM_BOUNDS:
            if name.startswith(char):
                name, keep_looking = name[len(char):], True
            if name.endswith(char):
                name, keep_looking = name[:-len(char)], True
    if reencode:
        name = ftfy.ftfy(name)

    name = name.strip()  # Just in case " " would be not included in the list
    return name

def clean_translated_synopsis(synopsis: str) -> str:
    try:
        synopsis = re.sub(r'(?<!\.)\.\.(?!\.)', '.', synopsis)
    except TypeError as e:
        logger.error(f"Type error while cleaning synopsis")
    return synopsis

def delete_params_from_url(url: str) -> str:
    """
    Delete all the parameters from the url
    :param url: str. The url
    :return: str. The url without parameters
    """
    return url.split("?")[0]


def clean_movie_title(title: str) -> str:
    """
    Clean the movie title, removing all the unnecessary characters
    :param title: str. The title of the movie
    :return: str. The cleaned title of the movie
    """
    title = clean_name(name=title, reencode=True)
    # Find everything between parenthesis and remove it
    parenthesis = re.findall(r"\(.*?\)", title)
    for parenthesis_str in parenthesis:
        if parenthesis_str not in KNOWN_TITLE_PARENTHESIS_TO_DELETE:
            logger.warning(f"Found unknown parenthesis {parenthesis_str} in title {title}. Deleted")
            if "music" in parenthesis_str.lower():
                raise InvalidMovieException("It was a Musical Video")

        title = title.replace(parenthesis_str, "")
    title = title.strip()
    return title


def clean_synopsis(synopsis: str, lang: str, cast : tuple[str] = ()) -> str:
    """
    Clean the synopsis of the movie
    :param synopsis: str. The synopsis of the movie
    :return: str. The cleaned synopsis of the movie
    """
    synopsis = clean_name(name=synopsis, reencode=True)
    # Find every match in the array REGEX_TO_DELETE_FROM_SYNOPSIS
    to_delete = re.findall(fr"({'|'.join(REGEX_TO_DELETE_FROM_SYNOPSIS)})", synopsis)
    for to_delete_str in to_delete:
        synopsis = clean_name(name=synopsis.replace(to_delete_str, ""), reencode=True)
        if synopsis == "":
            logger.warning(f"Found empty synopsis after deleting {to_delete_str}")
            break

    for person in cast:
        if f"({person})" in synopsis:
            synopsis = synopsis.replace(f"({person})", "").replace("  ", " ")

    detect_potential_copyright(synopsis=synopsis, lang=lang, cast=cast)

    return synopsis


def detect_potential_copyright(synopsis: str, lang: str, cast: tuple[str] = ()):

    nlp = NER_MODELS[lang]
    doc = nlp(synopsis)
    entities = doc.ents
    if len(entities) == 0:
        return synopsis
    # If last entity is a person, pay attention
    last_entity = entities[-1]
    known_within_text_names = [entity.text for entity in entities[:-1] if entity.label_ in ("PERSON", "PER")]
    # Add single words for detecting names and surnames altogether or separately
    known_within_text_names += [name for entity in known_within_text_names for name in entity.split()]
    if last_entity.label_ in ("PERSON", "PER") and last_entity.text not in cast and last_entity.text not in known_within_text_names:
        # Delete it.
        if last_entity.end_char >= len(synopsis) - len(last_entity.text):
            raise InvalidMovieException(f"Potential Copyright on Synopsis for ({last_entity.text}): {synopsis}")
            #synopsis = synopsis[:last_entity.end_char-len(last_entity.text)].strip() + "."



    return synopsis
