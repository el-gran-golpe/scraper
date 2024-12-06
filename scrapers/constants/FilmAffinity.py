import os

from nlp.languages import ENGLISH, SPANISH, CATALAN, DEUTSCH


class InvalidMovieException(Exception):
    pass


BASE_WEB = "https://www.filmaffinity.com/en/"
TRANSLATIONS_BATCH_SIZE = 96
BACKUP_FILM_DATABASE_EVERY = 4

DELETE_ENTRY_MARK = "DELETE ALL"
TOPICS_TO_DELETE = ("Music Video", "Narrative Videogame", "Branded Content Short Film")

# DICT KEYS

URL = "url"
ID = "id"
TITLE = "title"
TEXT = "text"
AWARD = "award"
TO = "to"

# BASIC INFO
BASIC_INFO = "basic_info"
ORIGINAL_TITLE = "original_title"
SLUG = "slug"
DURATION_MINUTES = "duration_minutes"
COUNTRY = "country"
COUNTRIES = "countries"
YEAR = "year"
GENRES = "genres"
TOPICS = "topics"
ORIGINAL_LANGS = "original_langs"

AVAILABLE_AT = "available_at"
ALTERNATIVE_MULTIMEDIA = "alternative_multimedia"
AVAILABLE_AT_PLATFORMS = 'platforms'
AVAILABLE_AT_PLATFORM = 'platform'
AVAILABLE_AT_PLATFORM_MONETIZATION = 'platform_monetization'

# STAFF
STAFF = "staff"
DIRECTORS = "directors"
SCREENWRITERS = "screenwriters"

CAST = "cast"
PRODUCERS = "producers"
MUSICIANS = "musicians"
CINEMATOGRAPHERS = "cinematographers"

NAME = "name"
LANGUAGE = "lang"
ROLE = "role"

# FILM AFFINITY INFO
FILM_AFFINITY_INFO = "film_affinity_info"
SCORE = "score"
AVERAGE_SCORE = "average"
VOTES = "votes"
REVIEWS_COUNT = "reviews_count"

ENGLISH_TITLE = "english_title"
OTHER_TITLES = "other_titles"
SYNOPSIS = "synopsis"
SHORT_SYNOPSIS = "short_synopsis"
RATING = "rating"
OTHER_LINKS = "links"

# EXTENDED INFO
EXTENDED_INFO = "extended_info"
NOMINATIONS = "nominations"
RELEVANT_LINKS = "relevant_links"
POSTER_URL = "poster_url"
TRAILER_URL = "trailer_url"
PUBLICATION_DATE = "publication_date"

# AVAILABLE AT
JUST_WATCH = "just_watch"
STREAMING = "streaming"
BUY = "buy"
ADS = "free_with_ads"
RENT = "rent"
FREE = "free"


# LANGUAGES
PENDING_TO_TRANSLATE = "pending_to_translate"
FILM_AFFINITY_SYNOPSIS = "film_affinity_synopsis"
JUST_WATCH_SYNOPSIS = "just_watch_synopsis"
REPHRASED_SYNOPSIS = "rephrased_synopsis"
LANGUAGES = "languages"

# STRUCTURES
BASIC_INFO_CONTENT = (ORIGINAL_TITLE, OTHER_TITLES, YEAR, DURATION_MINUTES, COUNTRY, GENRES, TOPICS)
STAFF_CONTENT = (DIRECTORS, CAST, PRODUCERS, MUSICIANS, CINEMATOGRAPHERS, SCREENWRITERS)

EXTRA_CAST_KEYS = ('#', 'uncredited', "G.I")
JUST_WATCH_LINKS_TO_AVOID = ('gdpr.tubi', )

VALID_DIRECTORS_MORE_INFO = {"(Creator)": "creator"}
VALID_STAFF_MORE_INFO = {"Novel": "writer (novel)", "Manga": "writer (manga)", "Poem" : "writer (poem)", "Graphic novel": "writer (comic)",
                         "Poems": "writer (poem)", "Essay": "writer (essay)", "Original story": "writer (original story)", "Original Story": "writer (original story)",
                         "Stories": "writer (stories)", "Books": "writer (book)","Original script": "Original script", "relatos": "writer (stories)",
                         'Original Series': 'writer (original story)',
                         "Arrangements": "music arrangements", "Biopic about": "biopic protagonist",
                         "Dialogues" : "dialogues", "Story": "story", "Plot": "plot", "Book": "writer (book)",
                         "Producer" : "producer", "Record Label": "producer", "Self" : "self", "Distributor" : "distributor", "Broadcast by" : "broadcaster",
                         "Remake" : "remake", "Cameo": "cameo", "Storyboard": "storyboard", "Characters" : "characters",
                         "Comic" : "writer (comic)", "Idea": "idea", "Theater": "writer (theater)", "Author": "author", "Videogame": "videogame",
                         "Play": "writer (play)", "Voice": "voice", "Novels": "writer (novel)", "Biography": "writer (biography)",
                         "adapt": "writer (adaptation)",
                         "Main theme": "main theme", "Graphic novels": "writer (comic)", "Director": "director",
                         "Character": "character", "Tale": "writer (tale)", "Tales": "writer (tale)", "Short Tale": "writer (tale)", "Libretto" : "writer (libretto)",
                         "Theme": "music theme", "Themes": "music theme", "Main Theme": "music theme", "Song": "main song", "Main song": "main song",
                         "Lyrics": "music theme",
                         "Opening music": "main song", "Franchise created by": "franchise creator",
                         "wmusical": "music theme", "Songs": "main song", "Additional music": "additional music",
                         "Non original music": "non original music", "Memoirs": "writer (biography)", "Text": "text", "Texts": "text",
                         "TV Series": "writer (tv series)", "Autobiography": "writer (autobiography)", "Opera": "opera",
                         "Restored version": "restored version", "opretta": "opera", "Article": "writer (article)",
                         "Original music": "original music"}

# AWARDS
KNOWN_AWARDS = {
    "Satellite Award": "Satellite",
    "Saturn Award": "Saturn",
    "Genie Award": "Genie",
    "Awards Genie": "Genie",
    "American Film Institute": "American Film Institute",
    "Emmy": "Emmy",
    "Golden Globe": "Golden Globe",
    "Golden Camera, Germany": "Golden Camera",
    "Oscar": "Oscar",
    "Óscar": "Oscar",
    "Goya Award": "Goya",
    "Goya": "Goya",
    "Cesar Award": "Cesar",
    "César": "Cesar",
    "Cesar": "Cesar",
    "Nominated for Cesar": "Cesar",
    "César Award": "Cesar",
    "Animayo": "Animayo",
    "Academy Award": "Academy",
    "Platino Award": "Platino",
    "National Academy of Video Game Trade Reviewers": "National Academy of Video Game Trade Reviewers",
    "Premios de la Academia Japonesa": "Japanese Academy",
    "Producers Guild Award": "Producers Guild of America",
    "Writers Guild of America": "Writers Guild of America",
    "Writers Guild Award": "Writers Guild of America",
    "Directors Guild of America": "Directors Guild of America",
    "Screen Actors Guild": "Screen Actors Guild",
    "Critics Choice Award": "Critics Choice",
    "Critics' Choice Award": "Critics Choice",
    "Blue Dragon Film Awards (South Korea)": "Blue Dragon",
    "Razzie Award": "Razzie",
    "Premios Razzie": "Razzie",
    "Gotham Award": "Gotham",
    "Premios Gotham": "Gotham",
    "Annie": "Annie",
    "Annie Award": "Annie",
    "Sur Award": "Sur",
    "Macondo Award": "Macondo",
    "David di Donatello Award": "David di Donatello",
    "Independent Spirit Award": "Independent Spirit",
    "European Film Award": "European Film",
    "European Film Awads": "European Film",
    "Méliès": "Melies",
    "NAACP Image Awards": "NAACP Image",
    "Sundance Film Festival": "Sundance Film Festival",
    "Sundance": "Sundance Film Festival",
    "Film Festival of Catalonia": "Catalonia Film Festival",
    "Ottawa International Animation Festival": "Ottawa International Animation Festival",
    "Cairo International Film Festival": "Cairo International Film Festival",
    "Cairo": "Cairo International Film Festival",
    "Cairo Film Festival": "Cairo International Film Festival",
    "Cannes Film Festival": "Cannes Film Festival",
    "Cannes": "Cannes Film Festival",
    "Toronto Film Festival": "Toronto Film Festival",
    "Toronto International Film Festival": "Toronto Film Festival",
    "Avoriaz International Fantastic Film Festival": "Avoriaz Fantastic Film Festival",
    "Festival Toronto": "Toronto Film Festival",
    "Tokyo Film Festival": "Tokyo Film Festival",
    "Tokyo International Film Festival": "Tokyo Film Festival",
    "Biarritz Film Festival": "Biarritz Film Festival",
    "Venice Film Festival": "Venice Film Festival",
    "Venice": "Venice Film Festival",
    "SXSW": "SXSW Film Festival",
    "Valladolid International Film Festival": "Valladolid International Film Festival",
    "Valladolid Film Festival": "Valladolid International Film Festival",
    "Valladolid": "Valladolid International Film Festival",
    "Gijon Film Festival": "Gijon Film Festival",
    "Gijón Film Festival": "Gijon Film Festival",
    "Málaga Film Festival": "Malaga Film Festival",
    "Malaga Film Festival": "Malaga Film Festival",
    "Fantasporto Film Festival": "Fantasporto Film Festival",
    "Málaga": "Malaga Film Festival",
    "San Sebastian Film Festival": "San Sebastian Film Festival",
    "San Sebastián": "San Sebastian Film Festival",
    "San Sebastian": "San Sebastian Film Festival",
    "Sevilla Film Festival": "Sevilla Film Festival",
    "Seville Film Festival": "Sevilla Film Festival",
    "Seville European Film Festival": "Sevilla Film Festival",
    "Moscow Film Festival": "Moscow Film Festival",
    "Moscow International Film Festival": "Moscow Film Festival",
    "Rotterdam Film Festival": "Rotterdam Film Festival",
    "Rotterdam International Film Festival": "Rotterdam Film Festival",
    "Rome Film Festival": "Rome Film Festival",
    "Tribeca Film Festival": "Tribeca Film Festival",
    "Berlin Film Festival": "Berlin Film Festival",
    "Berlín Film Festival": "Berlin Film Festival",
    "Berlin": "Berlin Film Festival",
    "Berlin International Film Festival": "Berlin Film Festival",
    "Chicago International Film Festival": "Chicago International Film Festival",
    "Chicago Film Festival": "Chicago International Film Festival",
    "Habana Film Festival": "Habana Film Festival",
    "Sitges Film Festival": "Sitges Film Festival",
    "Sitges Fantasy Film Festival": "Sitges Film Festival",
    "SXSW Film Festival": "South by Southwest Film Festival",
    "Fénix Film Awards - Latin-America": "Fenix Film",
    "Festival Cinema Fantasy of Sitges": "Sitges Film Festival",
    "Sitges": "Sitges Film Festival",
    "Seminci Film Festival": "Seminci Film Festival",
    "Sarajevo Film Festival": "Sarajevo Film Festival",
    "Seminci": "Seminci Film Festival",
    "Shanghai Film Festival": "Shanghai Film Festival",
    "Quirino Awards": "Quirino",
    "MTV Music Video Awards": "MTV Music Video",
    "MTV Europe Music Video Awards": "MTV Music Video",
    "Hamptons Film Festival": "Hamptons Film Festival",
    "Hamptons International Film Festival": "Hamptons Film Festival",
    "Mar del Plata Film Festival": "Mar del Plata Film Festival",
    "Mar del Plata International Film Festival": "Mar del Plata Film Festival",
    "Karlovy Vary International Film Festival": "Karlovy Vary International Film Festival",
    "Karlovy Vary Internacional Film Festival": "Karlovy Vary International Film Festival",
    "Karlovy Vary Film Festival": "Karlovy Vary International Film Festival",
    "Karlovy Vary": "Karlovy Vary International Film Festival",
    "Annecy Film Festival": "Annecy Film Festival",
    "Annecy": "Annecy Film Festival",
    "Festival Annecy": "Annecy Film Festival",
    "Ondas Awards": "Ondas",
    "Montréal World Film Festival": "Montreal World Film Festival",
    "Morelia": "Morelia Film Festival",
    "London Film Festival": "London Film Festival",
    "Locarno Film Festival": "Locarno Film Festival",
    "Festival Locarno": "Locarno Film Festival",
    "Locarno International Film Festival": "Locarno Film Festival",
    "Havana Film Festival": "Havana Film Festival",
    "Shanghai International Film Festival": "Shanghai Film Festival",
    "Chicago International Children's Film Festival": "Chicago International Children's Film Festival",
    "Feroz Award": "Feroz",
    "Ariel Award": "Ariel",
    "Ariel ward": "Ariel",
    "BAFTA TV": "Bafta",
    "BAFTA Award": "Bafta",
    "BAFTA": "Bafta",
    "BAFICI": "Bafici",
    "AACTA Award": "Aacta",
    "Forqué Award": "Forque",
    "Göteborg Film Festival": "Goteborg Film Festival",
    "FICUNAM": "Ficunam",
    "Swiss Film Award": "Swiss Film",
    "New York Videogame Critics Circle" : "New York Videogame Critics Circle",
    "National Board of Review": "National Board of Review",
    "National Board Review": "National Board of Review",
    "National Society of Film Critics (NSFC)": "National Society of Film Critics",
    "New York Film Critics Circle": "New York Film Critics Circle",
    "British Independent Film Award": "British Independent Film",
    "Los Angeles Film Critics Association": "Los Angeles Film Critics Association",
    "Los Angeles Films Critics Association": "Los Angeles Film Critics Association",
    "Television Critics Association Award": "Television Critics Association",
    "Gaudí Award": "Gaudi",
    "The Game Awards": "Game Awards",
    "German Film Award": "German Film",
    "German Film Awards": "German Film",
    "los Awards from CFinema German": "German Film",
    "Canadian Screen Awards": "Canadian Screen",
    "Chicago Film Critics Award": "Chicago Film Critics Association",
    "Chicago Films Critics Awards": "Chicago Film Critics Association",
    "Chicago Film Critics Association": "Chicago Film Critics Association",
    "Film Critics Circle of New York": "Film Critics Circle of New York",
    "Boston Society of Film Critics": "Boston Society of Film Critics",
    "Boston Film Critic": "Boston Society of Film Critics",
    "Paris International Fantastic Film Festival (PIFFF)": "Paris Fantastic Film Festival",
    "Boston Independent Film Festival": "Boston Film Festival",
    "San Francisco Film Critics Circle": "San Francisco Film Critics Circle",
    "Guldbagge Award": "Guldbagge",

}

assert len(KNOWN_AWARDS) == len(set(KNOWN_AWARDS)), "There are repeated awards"

KNOWN_AWARDS_LOWERCASE = {k.lower(): v for k, v in KNOWN_AWARDS.items()}

FIRST_FILM_AFFINITY_YEAR = 2010

# JSON FILES
RESOURCES_PATH = os.path.join("resources", "FilmAffinity")
DATABASES_PATH = os.path.join(RESOURCES_PATH, "databases")

COUNTRIES_JSON = os.path.join(RESOURCES_PATH, "countries.json")
MAIN_GENRES_JSON = os.path.join(RESOURCES_PATH, "main_genres.json")

CHARACTERS_TO_REMOVE_FROM_BOUNDS = ["\t", "\n", "\r", ".", '"', "*", "/", "|", " ", ";", "&nbsp;", ":", "(FILMAFFINITY)", " 3D"]

RELEVANT_LINKS_URL_TO_SITE = {
    "en.wikipedia.org": {NAME : "Wikipedia", LANGUAGE: ENGLISH},
    "es.wikipedia.org": {NAME : "Wikipedia", LANGUAGE: SPANISH},
    "hallmarkchannel.com": {NAME : "Hallmark Channel", LANGUAGE: ENGLISH},
    "hallmarkmoviesandmysteries.com": {NAME : "Hallmark Channel", LANGUAGE: ENGLISH},
    "paco-magic.com": {NAME : "Film Website", LANGUAGE: ENGLISH},
    "fivestarthemovie.com": {NAME : "Film Website", LANGUAGE: ENGLISH},
    "schneemannfoundation.org": {NAME : "Schneemann Foundation", LANGUAGE: ENGLISH},
    "yidff.jp" : {NAME : "YIDFF", LANGUAGE: ENGLISH},
    "cinemargentino.com": {NAME : "Cinema Argentino", LANGUAGE: SPANISH},
    "facebook.com": {NAME : "Facebook", LANGUAGE: ENGLISH},
    "fandom.com/es": {NAME : "Fandom", LANGUAGE: SPANISH},
    "fandom.com/en": {NAME : "Fandom", LANGUAGE: ENGLISH},
    "rtve.es": {NAME : "RTVE", LANGUAGE: SPANISH},
    "lux.org.uk": {NAME : "Lux", LANGUAGE: ENGLISH},
    "freews.es": {NAME : "FreeWS", LANGUAGE: SPANISH},
    "holtsmithsonfoundation.org": {NAME : "Holtsmithson Foundation", LANGUAGE: ENGLISH},
    "jpixx.com": {NAME : "JPixx", LANGUAGE: ENGLISH},
    "goforsistersmovie.com" : {NAME : "Film Website", LANGUAGE: ENGLISH},
    "amyhalpern.com": {NAME : "Director Website", LANGUAGE: ENGLISH},
    "makinotakashi.net": {NAME : "Director Website", LANGUAGE: ENGLISH},
    "julesverne.org": {NAME : "Jules Verne", LANGUAGE: ENGLISH},
    "sonyclassics.com": {NAME : "Sony", LANGUAGE: ENGLISH},
    ".der.org": {NAME : "Documentary Educational Resources", LANGUAGE: ENGLISH},
    "checkoofilm.com": {NAME : "Checkoofilm", LANGUAGE: ENGLISH},
    "siwaproductions.com": {NAME : "Siwa Productions", LANGUAGE: ENGLISH},
    ".nfb.ca": {NAME : "National Film Board of Canada", LANGUAGE: ENGLISH},
    "eduardocasanova.es": {NAME : "Director Website", LANGUAGE: SPANISH},
    "earthmuted.org": {NAME : "Film Website", LANGUAGE: ENGLISH},
    "nathanieldorsky.net": {NAME : "Director Website", LANGUAGE: ENGLISH},
    "elumiere.net": {NAME : "Elumiere Magazine", LANGUAGE: SPANISH},
    "davidandfatima.com": {NAME : "Film Website", LANGUAGE: ENGLISH},
    "fourfeathersmovie.com": {NAME : "Film Website", LANGUAGE: ENGLISH},
    "intimosrelatos.blogspot.mx": {NAME : "Film Website", LANGUAGE: SPANISH},
    "13hoursmovie.com": {NAME : "Film Website", LANGUAGE: ENGLISH},
    "elinmigrantemovie.com": {NAME : "Film Website", LANGUAGE: SPANISH},
    "losamantespasajeros.com": {NAME : "Film Website", LANGUAGE: SPANISH},
    "canyoncinema.com": {NAME : "Canyon Cinema", LANGUAGE: ENGLISH},
    "store.steampowered.com": {NAME : "Steam", LANGUAGE: ENGLISH},
    "protoncinema.hu": {NAME : "Proton Cinema", LANGUAGE: ENGLISH},
    "TeenageDramaQueen.com": {NAME : "Film Website", LANGUAGE: ENGLISH},
    "sarahvandenboom.fr": {NAME : "Director Website", LANGUAGE: ENGLISH},
    "tumblr.com": {NAME : "Tumblr", LANGUAGE: ENGLISH},
    "thechild-film.com": {NAME : "Film Website", LANGUAGE: ENGLISH},
    "freemanthemovie.wordpress.com": {NAME : "Film Website", LANGUAGE: ENGLISH},
    "naruto-movie.com": {NAME : "Film Website", LANGUAGE: ENGLISH},
    "viruete.com": {NAME : "Viruete", LANGUAGE: SPANISH},
    "danteshellanimated.com": {NAME : "Film Website", LANGUAGE: ENGLISH},
    "film-makerscoop.com": {NAME : "Film Makers Coop", LANGUAGE: ENGLISH},
    "agnisphilosophy.com": {NAME : "Film Website", LANGUAGE: ENGLISH},
    "filmoteca.cat": {NAME : "Filmoteca", LANGUAGE: CATALAN},
    "tate.org.uk": {NAME : "Tate", LANGUAGE: ENGLISH},
    "circomexico.com": {NAME : "Film Website", LANGUAGE: SPANISH},
    "afternoondelightfilm.com": {NAME : "Film Website", LANGUAGE: ENGLISH},
    "beetlequeen.com": {NAME : "Film Website", LANGUAGE: ENGLISH},
    "magnetreleasing.com": {NAME : "Magnet Releasing", LANGUAGE: ENGLISH},
    "myarchitectfilm.com": {NAME : "Film Website", LANGUAGE: DEUTSCH},
    "breakfastwithcurtis.com": {NAME : "Film Website", LANGUAGE: ENGLISH},
    "americancasinothemovie.com": {NAME : "Film Website", LANGUAGE: ENGLISH},
    "orsonwest.com": {NAME : "Film Website", LANGUAGE: ENGLISH},
    "darkeningsky.com": {NAME : "Film Website", LANGUAGE: ENGLISH},
    "thetenantthemovie.com": {NAME : "Film Website", LANGUAGE: ENGLISH},
    "cargocollective.com": {NAME : "Cargo Collective", LANGUAGE: ENGLISH},
    "thepeoplescloud.org": {NAME : "Film Website", LANGUAGE: ENGLISH},
    "warnerbros.com": {NAME : "Warner Bros", LANGUAGE: ENGLISH},
    "iwantcandymovie.com": {NAME : "Film Website", LANGUAGE: ENGLISH},
    "zmdthemovie.com": {NAME : "Film Website", LANGUAGE: ENGLISH},
    "shootemupmovie.com": {NAME : "Film Website", LANGUAGE: ENGLISH},
    "alexandrelarose.com": {NAME : "Director Website", LANGUAGE: ENGLISH},
    "cjcinema.org": {NAME : "CJ Cinema", LANGUAGE: ENGLISH},
    "sonypictures.com": {NAME : "Sony Pictures", LANGUAGE: ENGLISH},
    "expcinema.org": {NAME : "Experimental Cinema", LANGUAGE: SPANISH},
    "davidblyth.com": {NAME : "Director Website", LANGUAGE: ENGLISH},
    "goodfilmscollective.com": {NAME : "Good Films Collective", LANGUAGE: ENGLISH},
}

RELEVANT_LINKS_TO_AVOID = ("netflix.com",  "nbc.com", "pureflix.com", "thefilmdetective.tv", "mitele.es", "claraderfilm.com",
                           "blog.naver.com", "vimeo.com", "imvbox.com", "laurits.com", "elmaldelarriero.com", "bbc.co.uk",
                           "blog.goo.ne.jp", "neptunofilms.com", "lightcone.org", ".ne.jp", "imageforum.co.jp", "dreamcreation.co.jp",
                           "cinematoday.jp","seekthesigns.com", "altafilms.com", "sobooks.jp", "pjmia.wordpress.com", "re-voir.com",
                           "frischgepresst-derfilm.de", "tennoshizuku.com", "mgm.com", "alain-mazars.fr", "bensteer.com", "cccb.org", "archive.org",
                           "fenix1123.cat", "disney.go.com", "google.com", "entradasfilmoteca.gob.es", "s8cinema.com", "abel-lapelicula.com",
                           "neighborhoodwatchthefilm.com", "evangelion.co.jp", "lecumedesjours-lefilm.com", "thestoning.com",
                           "jamesedmonds.org", "marv.jp", "swissfilms.ch")



AVAILABLE_AT_PLATFORMS_TO_AVOID = ("Redbox", "YouTube", "Freevee Amazon Channel", "Vudu", "VUDU Free", "DIRECTV")
AVAILABLE_AT_DELETE_PARAMS_PLATFORMS = ("Apple iTunes", "Amazon Video", "Hulu", "Pluto TV")

KNOWN_TITLE_PARENTHESIS_TO_DELETE = ('(S)', '(TV Series)', '(TV Miniseries)', '(Serie de TV)', "(Miniserie de TV)", "(TV)", "(C)")

REGEX_TO_DELETE_FROM_SYNOPSIS = ('TV Series \(\d+-?\)', 'TV Series \(\d+\s?-\s?Present Day\)', 'TV Series \(\d+\s?-\s?\d+\)',
                                '\d+\s?[S|s]easons', '\d+\s?[E|e]pisodes',
                                 '\d+\s?\w{2}\s?[S|s]eason release date: \d+\s?\w+\s?\d{4}', '\(\s?FILMAFFINITY\s?\)',
                                 'Confirmed a \d+\s?\w+ [S|s]eason', 'Release \d+\s?\w+\[S|s]eason:.*\.',
                                 # Spanish
                                 '[S|s]erie de TV \(\d+\s?-?\)', '[S|s]erie de TV \(\d+\s?-\s?[A|a]ctualidad\)', 'Serie de TV \(\d+\s?-\s?\d+\)',
                                 '\d+\s?[T|t]emporadas', '\d+\s?[E|e]pisodios',
                                 '[E|e]streno\s?\d+\w*\s?[T|t]emporada:\s?.*\.',
                                 "\([^\)]*[wW]ikipedia[^\)]*\)", "\[[^\]]*[wW]ikipedia[^\]]*\]")



FILM_AFFINITY_WEB_LANGS = (ENGLISH, SPANISH)
