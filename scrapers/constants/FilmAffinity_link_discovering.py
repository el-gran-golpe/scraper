import os
from scrapers.constants.FilmAffinity import DATABASES_PATH

ALL_FILMS_SEARCH = "search.php?stype=title&stext=&orderby=year"
ADVANCED_FILMS_SEARCH = "advsearch.php?page={page}&stype[]=title&country={country}&genre={genre}&fromyear={year}&toyear={year}"
ADVANCED_FILMS_SEARCH_WITHOUT_GENRE = "advsearch.php?page={page}&stype[]=title&country={country}&fromyear={year}&toyear={year}"

MAX_PAGES_PER_SEARCH = 25

# JSON PATHS (from root)

DISCOVERED_LINKS_JSON = os.path.join(DATABASES_PATH, "discovered_links.json")

# HTML ELEMENTS

MOVIE_CARD_CLASS = "movie-card"
MOVIE_CARD_ELEMENT = "div"
MOVIE_ID_ATTRIB = "data-movie-id"

MOVIE_TITLE_CLASS = "mc-title"
MOVIE_TITLE_FATHER_ELEMENT = "div"
MOVIE_TITLE_ELEMENT = "a"
MOVIE_TITLE_ATTRIB = "title"
MOVIE_URL_ATTRIB = "href"

# XPATHS

MOVIE_CARD_XPATH = f'//{MOVIE_CARD_ELEMENT}[contains(@class, "{MOVIE_CARD_CLASS}")]'
MOVIE_TITLE_ATTRIB_XPATH = f'.//{MOVIE_TITLE_FATHER_ELEMENT}[contains(@class, "{MOVIE_TITLE_CLASS}")]/' \
                              f'{MOVIE_TITLE_ELEMENT}'


NEXT_PAGE_WRAPPER_CLASS = "buttons-wrapper"
NEXT_PAGE_WRAPPER_ELEMENT = "div"
NEXT_PAGE_GRANDSON_CLASS = "see-all-button"
NEXT_PAGE_GRANDSON_ELEMENT = "div"
NEXT_PAGE_ELEMENT = "a"
NEXT_PAGE_ATTRIB = "href"

NEXT_PAGE_XPATH = f'//{NEXT_PAGE_WRAPPER_ELEMENT}[contains(@class, "{NEXT_PAGE_WRAPPER_CLASS}")]/{NEXT_PAGE_ELEMENT}/' \
                    f'{NEXT_PAGE_GRANDSON_ELEMENT}[contains(@class, "{NEXT_PAGE_GRANDSON_CLASS}")]/parent::{NEXT_PAGE_ELEMENT}'


AMOUNT_OF_PAGES_ADV_SEARCH_CLASS = "adv-search-page-info"
AMOUNT_OF_PAGES_ADV_SEARCH_ID = "adv-search-pager-info"
AMOUNT_OF_PAGES_ADV_SEARCH_ELEMENT = "div"
AMOUNT_OF_PAGES_ADV_SEARCH_PARENT_ELEMENT = "div"

AMOUNT_OF_PAGES_ADV_SEARCH_XPATH = f'//{AMOUNT_OF_PAGES_ADV_SEARCH_ELEMENT}[@id="{AMOUNT_OF_PAGES_ADV_SEARCH_ID}"]/' \
                                   f'{AMOUNT_OF_PAGES_ADV_SEARCH_ELEMENT}[contains(@class, "{AMOUNT_OF_PAGES_ADV_SEARCH_CLASS}")]'

CURRENT_AND_MAX_PAGES_ELEMENT = "b"
CURRENT_AND_MAX_PAGES_XPATH = f'./{CURRENT_AND_MAX_PAGES_ELEMENT}'