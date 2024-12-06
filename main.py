from urllib3 import HTTPSConnectionPool

from scrapers.FilmAffinity_link_discoverer import FilmAffinityLinkDiscoverer
from scrapers.FilmAffinity_films_inspector import FilmAffinityFilmsInspector
from time import time, sleep
from requests.exceptions import ReadTimeout, ConnectionError
from urllib3.exceptions import ReadTimeoutError
DISCOVER_LINKS = False



if __name__ == '__main__':

    if DISCOVER_LINKS:
        discoverer = FilmAffinityLinkDiscoverer()
        discoverer.fill_discovered_links_database(from_year=None)
    else:
        while True:
            try:
                # Scrap all the information of the web
                scraper = FilmAffinityFilmsInspector()
                scraper.fill_pending_films()
            except (ReadTimeout, ReadTimeoutError, ConnectionError) as e:
                print(f"Exception {e}. Waiting 2 hours before retrying")
                sleep(2*60*60)
            except AssertionError as e:
                print(f"ASSERTION: {e}")
                sleep(2*60*60)
            except ValueError as e:
                print("Value Error. Likely because of the rephrasing")
                sleep(1*60*60)