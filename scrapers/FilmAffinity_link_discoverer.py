from __future__ import annotations

import os
import shutil
from scrapers.FilmAffinity_parsers import get_max_pages, extract_movies_from_page, clean_name
from scrapers.constants.FilmAffinity_link_discovering import ALL_FILMS_SEARCH, \
    NEXT_PAGE_XPATH, NEXT_PAGE_ATTRIB, ADVANCED_FILMS_SEARCH, \
    DISCOVERED_LINKS_JSON, ADVANCED_FILMS_SEARCH_WITHOUT_GENRE, \
    MAX_PAGES_PER_SEARCH
from scrapers.constants.FilmAffinity import BASE_WEB, YEAR, FIRST_FILM_AFFINITY_YEAR, COUNTRIES_JSON, MAIN_GENRES_JSON

from scrapers.BaseScraper import BaseScraper
from lxml.html import HtmlElement
import json
from datetime import datetime
from loguru import logger

class FilmAffinityLinkDiscoverer(BaseScraper):
    """
    Class that extract all the information
    """
    def __init__(self, base_web: str = BASE_WEB):
        super().__init__()
        assert type(base_web) == str, f"Expected base_web to be a string, got {type(base_web)}"
        self.base_web = base_web
        self.countries = json.load(open(COUNTRIES_JSON, "r"))
        self.main_genres = json.load(open(MAIN_GENRES_JSON, "r"))

        if not os.path.exists(DISCOVERED_LINKS_JSON):
            logger.warning(f"Discovered links database not found. Creating new one")
            with open(DISCOVERED_LINKS_JSON, "w") as f:
                json.dump({}, f)
        self.discovered_links_database = json.load(open(DISCOVERED_LINKS_JSON, "r", encoding="utf-8"))

    def get_first_1000_new_films(self) -> dict[str, dict[str, str]]:
        """
        Get all the films from FilmAffinity
        :return: Dictionary. Dictionary with all the films in the format {id: {title: title, url: url}}
        """
        html = self.get(url=self.base_web + ALL_FILMS_SEARCH)
        films = {}
        while html is not None:
            films.update(self.extract_movies_from_page(html=html))
            # Get the next page
            next_page = html.xpath(NEXT_PAGE_XPATH)
            assert len(next_page) <= 1, f"Expected 0 or 1 next page, got {len(next_page)}"
            if len(next_page) == 1:
                url = next_page[0].attrib[NEXT_PAGE_ATTRIB]
                url = self.base_web + url
                html = self.get(url=url)
            else:
                html = None
        return films

    def fill_discovered_links_database(self, from_year:int | None = None) -> dict[str, dict[str, str]]:
        """
        Get all the films from FilmAffinity
        :return: Dictionary. Dictionary with all the films in the format {id: {title: title, url: url}}
        """
        first_year = from_year if from_year is not None else self.get_year_to_inspect()
        current_year = datetime.now().year
        for year in range(first_year, current_year + 1):
            for country_code, country_name in self.countries.items():
                # First, check if all genres can be read at once
                without_genre_search = ADVANCED_FILMS_SEARCH_WITHOUT_GENRE.format(page=1, country= country_code, year=year)
                html = self.get(url=self.base_web + without_genre_search)
                max_pages = get_max_pages(html=html)
                if max_pages is None:
                    logger.info(f"Country {country_name} ({country_code}) has no films in {year}")
                    continue
                elif max_pages < MAX_PAGES_PER_SEARCH:
                    main_genres = {"": "All Genres"}
                else:
                    assert max_pages == MAX_PAGES_PER_SEARCH, f"Expected max pages to be {MAX_PAGES_PER_SEARCH} or less," \
                                                              f" got {max_pages}"
                    main_genres = self.main_genres
                for genre_code, genre_name in main_genres.items():
                    if genre_code != "":
                        advanced_search = ADVANCED_FILMS_SEARCH.format(page=1, country=country_code, genre=genre_code, year=year)
                        html = self.get(url=self.base_web + advanced_search)
                        max_pages = get_max_pages(html=html, current_page=1)
                        if max_pages is None:
                            continue
                    for page in range(1, max_pages + 1):
                        if page > 1:
                            advanced_search = ADVANCED_FILMS_SEARCH.format(page=page, country=country_code, genre=genre_code, year=year)
                            html = self.get(url=self.base_web + advanced_search)
                        self.update_database_with_page(html=html, year=year, country_code=country_code)
            self.backup_database()
            logger.info(f"Finished year: {year}/{current_year}")
        return self.discovered_links_database

    def update_database_with_page(self, html: HtmlElement, year:int, country_code:str) -> None:
        """
        Update the database with the movies in the page
        :param html: HtmlElement. Html of the page
        """
        assert len(country_code) == 2, f"Country code must be 2 characters long. Got {country_code}"
        new_films = extract_movies_from_page(html=html, year=year, country=country_code)
        # Sanity check that new films keep the same format
        repeated_films = tuple(id for id in new_films if id in self.discovered_links_database)
        for film in repeated_films:
            if not all(clean_name(name=str(self.discovered_links_database[film][key]), reencode=True) == str(new_films[film][key])
                       for key in self.discovered_links_database[film]):
                logger.warning(f"Previous film: {self.discovered_links_database[film]}, new film: {new_films[film]}")
                input(f"They both have different information. Press enter to continue")
        self.discovered_links_database.update(new_films)

    def get_year_to_inspect(self) -> int:
        """
        Get the last year that was inspected
        :return: int. Last year that was inspected
        """
        if len(self.discovered_links_database) == 0:
            return FIRST_FILM_AFFINITY_YEAR
        else:
            max_year = self.max_discovered_year()
            current_year = datetime.now().year
            if max_year >= current_year:
                logger.info(f"Database is up to date. Last year inspected: {max_year}")
            return min(max_year+1, current_year)

    def backup_database(self, verbose:bool = True) -> None:
        """
        Backup the database to a json file
        """
        if verbose:
            logger.info(f"Backing up database...")
        # First copy the current json file to a temp file
        temp_file = DISCOVERED_LINKS_JSON + ".temp"
        shutil.copyfile(DISCOVERED_LINKS_JSON, temp_file)
        # Then overwrite the json file with the new data
        try:
            with open(DISCOVERED_LINKS_JSON, "w", encoding="utf-8") as file:
                json.dump(self.discovered_links_database, file, indent=4, ensure_ascii=False)
        except Exception as e:
            # If something goes wrong, restore the old json file
            shutil.copyfile(temp_file, DISCOVERED_LINKS_JSON)
            raise e
        # Finally remove the temp file
        os.remove(temp_file)
        if verbose:
            logger.info(f"Database backed up. Current size: {len(self.discovered_links_database)} films")

    def max_discovered_year(self, default:int = FIRST_FILM_AFFINITY_YEAR) -> int:
        """
        Get the maximum year of the discovered films
        :return: int. Maximum year of the discovered films
        """
        if len(self.discovered_links_database) == 0:
            logger.warning("There are no films in the database")
            return default
        else:
            return max(film[YEAR] for film in self.discovered_links_database.values())