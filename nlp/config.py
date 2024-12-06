# LANGUAGES
from nlp.languages import *

TASK = "task"
MODEL = "model"
INITIAL_TOKEN = "initial_token"
MULTIPLE_LANGUAGES = "mul"
SOURCE_LANGUAGE = "source_language"
TRANSLATION_MODEL = "translation_model"
IMPROVED = "improved"
IMPROVED_TITLE = "improved_title"
SCORE = "score"

PIPELINE_PARAMS = {
    (SPANISH, ENGLISH): {
            TASK: "translation",
            MODEL: f"Helsinki-NLP/opus-mt-{SPANISH}-{ENGLISH}",
            INITIAL_TOKEN: "",
            SCORE: 4,
        },
    (ENGLISH, CHINESE): {
            TASK: "translation",
            MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{CHINESE}",
            INITIAL_TOKEN: "",
            SCORE: 3,
        },

    (ENGLISH, SPANISH): {
        TASK: "translation",
        MODEL: f"Helsinki-NLP/opus-mt-tc-big-{ENGLISH}-cat_oci_spa",
        INITIAL_TOKEN: ">>spa<<",
        SCORE: 5,
    },
    (ENGLISH, FRENCH): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-tc-big-{ENGLISH}-{FRENCH}",
        INITIAL_TOKEN: "",
        SCORE: 4.5,
    },
    (ENGLISH, BENGALI): {
        TASK: f"translation",
        MODEL: f"csebuetnlp/banglat5_nmt_{ENGLISH}_{BENGALI}",
        INITIAL_TOKEN: "",
        SCORE: 4,
    },
    (ENGLISH, RUSSIAN): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-tc-big-{ENGLISH}-zle",
        INITIAL_TOKEN: ">>rus<<",
        SCORE: 4.5,
    },
    (ENGLISH, PORTUGUESE): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-tc-big-{ENGLISH}-{PORTUGUESE}",
        INITIAL_TOKEN: ">>por<<",
        SCORE: 4.5,
    },
    (ENGLISH, INDONESIAN): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{INDONESIAN}",
        INITIAL_TOKEN: "",
        SCORE: 3,
    },
    (ENGLISH, ARABIC): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-tc-big-{ENGLISH}-{ARABIC}",
        INITIAL_TOKEN: "",
        SCORE: 4.5,
    },

    (ENGLISH, JAPANESE): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-tatoeba-{ENGLISH}-{JAPANESE}",
        INITIAL_TOKEN: "",
        SCORE: 3,
    },
    (ENGLISH, DEUTSCH): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{DEUTSCH}",
        INITIAL_TOKEN: "",
        SCORE: 4.5,
    },
    (ENGLISH, JAVANESE): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{MULTIPLE_LANGUAGES}",
        INITIAL_TOKEN: ">>jav<<",
        SCORE: 3,
    },

    (ENGLISH, TURKISH): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-tc-big-{ENGLISH}-{TURKISH}",
        INITIAL_TOKEN: "",
        SCORE: 4.5
    },

    (SPANISH, ITALIAN): {
        TASK: "translation",
        MODEL: f"Helsinki-NLP/opus-mt-{SPANISH}-{ITALIAN}",
        INITIAL_TOKEN: "",
        SCORE: 4,
    },

    (ENGLISH, SWEDISH): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{SWEDISH}",
        INITIAL_TOKEN: "",
        SCORE: 3.5,
    },
    (ENGLISH, FINNISH): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-tc-big-{ENGLISH}-{FINNISH}",
        INITIAL_TOKEN: "",
        SCORE: 4.5,
    },
    (ENGLISH, DUTCH): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{DUTCH}",
        INITIAL_TOKEN: "",
        SCORE: 4.5
    },
    (ENGLISH, UKRAINIAN): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-tc-big-{ENGLISH}-zle",
        INITIAL_TOKEN: ">>ukr<<",
        SCORE: 4.5,
    },
    (SPANISH, POLISH): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{SPANISH}-{POLISH}",
        INITIAL_TOKEN: "",
        SCORE: 4,
    },
    (ENGLISH, DANISH): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{DANISH}",
        INITIAL_TOKEN: "",
        SCORE: 4.5,
    },
    (ENGLISH, BULGARIAN): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-tc-big-{ENGLISH}-{BULGARIAN}",
        INITIAL_TOKEN: "",
        SCORE: 4.5,
    },
    (ENGLISH, CZECH): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-tc-big-{ENGLISH}-ces_slk",
        INITIAL_TOKEN: ">>ces<<",
        SCORE: 4,
    },
    (ENGLISH, GREEK): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-tc-big-{ENGLISH}-{GREEK}",
        INITIAL_TOKEN: "",
        SCORE: 4,
    },
    (ENGLISH, ICELANDIC): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{ICELANDIC}",
        INITIAL_TOKEN: "",
        SCORE: 3
    },
    (SPANISH, CROATIAN): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{SPANISH}-{CROATIAN}",
        INITIAL_TOKEN: "",
        SCORE: 3,
    },
    (ENGLISH, HUNGARIAN): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-tc-big-{ENGLISH}-{HUNGARIAN}",
        INITIAL_TOKEN: "",
        SCORE: 3,
    },
    (SPANISH, SLOVENIAN): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{SPANISH}-{SLOVENIAN}",
        INITIAL_TOKEN: "",
        SCORE: 4
    },
    (SPANISH, LITHUANIAN): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{SPANISH}-{LITHUANIAN}",
        INITIAL_TOKEN: "",
        SCORE: 3.5
    },
    (ENGLISH, ALBANIAN): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{ALBANIAN}",
        INITIAL_TOKEN: "",
        SCORE: 4,
    },
    (ENGLISH, ESTONIAN): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-tc-big-{ENGLISH}-{ESTONIAN}",
        INITIAL_TOKEN: "",
        SCORE: 4,
    },
    (ENGLISH, BELARUSIAN): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-tc-big-{ENGLISH}-zle",
        INITIAL_TOKEN: ">>bel<<",
        SCORE: 4,
    },

    (ENGLISH, MACEDONIAN): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{MACEDONIAN}",
        INITIAL_TOKEN: "",
        SCORE: 3
    },
    (ENGLISH, SLOVAK): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-tc-big-{ENGLISH}-ces_slk",
        INITIAL_TOKEN: ">>slk<<",
        SCORE: 3.5,
    },

    (ENGLISH, ARMENIAN): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{ARMENIAN}",
        INITIAL_TOKEN: "",
        SCORE: 2.5,
    },
    (SPANISH, CATALAN): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{SPANISH}-{CATALAN}",
        INITIAL_TOKEN: "",
        SCORE: 4.5,
    },
    (SPANISH, BASQUE): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{SPANISH}-{BASQUE}",
        INITIAL_TOKEN: "",
        SCORE: 4,
    },
    (SPANISH, GALICIAN): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{SPANISH}-{GALICIAN}",
        INITIAL_TOKEN: "",
        SCORE: 4.5,
    },

    (ENGLISH, LINGALA): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{LINGALA}",
        INITIAL_TOKEN: "",
        SCORE: 3
    },

    (ENGLISH, AFRIKAANS): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{AFRIKAANS}",
        INITIAL_TOKEN: "",
        SCORE: 3.5,
    },
    (ENGLISH, SWAHILI): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{SWAHILI}",
        INITIAL_TOKEN: "",
        SCORE: 3.5
    },
    (ENGLISH, MALAYALAM): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-dra",
        INITIAL_TOKEN: ">>mal<<",
        SCORE: 3,
    },

    (ENGLISH, LATVIAN): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-tc-big-{ENGLISH}-{LATVIAN}",
        INITIAL_TOKEN: "",
        SCORE: 4
    },

    (ENGLISH, XHOSA): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{XHOSA}",
        INITIAL_TOKEN: "",
        SCORE: 4,
    },
    (ENGLISH, TAGALOG): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{TAGALOG}",
        INITIAL_TOKEN: "",
        SCORE: 4,
    },
    (ENGLISH, AMHARIC): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-afa",
        INITIAL_TOKEN: ">>amh<<",
        SCORE: 3.5,
    },

    (ENGLISH, MALTESE): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{MALTESE}",
        INITIAL_TOKEN: "",
        SCORE: 3,
    },

    (ENGLISH, GANDA): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{GANDA}",
        INITIAL_TOKEN: "",
        SCORE: 3,
    },
    (ENGLISH, MALAGASY): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{MALAGASY}",
        INITIAL_TOKEN: "",
        SCORE: 3.5
    },

    (ENGLISH, ZULU): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-nic",
        INITIAL_TOKEN: ">>zul<<",
        SCORE: 3.5
    },
}

SOURCE_LANG_FROM_TARGET = {target: source for (source, target) in PIPELINE_PARAMS.keys()}
assert len(SOURCE_LANG_FROM_TARGET) == len(PIPELINE_PARAMS), f"Duplicate target languages"

"""
(ENGLISH, HINDI): {
    TASK: "translation",
    MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{HINDI}",
    INITIAL_TOKEN: "",
    SCORE: 2.5,
},
"""

"""
(ENGLISH, SAMOAN): {
    TASK: f"translation",
    MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{SAMOAN}",
    INITIAL_TOKEN: "",
    SCORE: 3
},
"""

"""
(ENGLISH, SHONA): {
    TASK: f"translation",
    MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{SHONA}",
    INITIAL_TOKEN: "",
    SCORE: 3
},
"""

"""
(ENGLISH, SOMALI): {
    TASK: f"translation",
    MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-afa",
    INITIAL_TOKEN: ">>som<<",
    SCORE: 3,
},
"""
"""
(ENGLISH, KINYARWANDA): {
    TASK: f"translation",
    MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{KINYARWANDA}",
    INITIAL_TOKEN: "",
    SCORE: 1.5
},
"""

"""
(ENGLISH, IGBO): {
    TASK: f"translation",
    MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{IGBO}",
    INITIAL_TOKEN: "",
    SCORE: 2.5
},
"""

"""
(ENGLISH, KANNADA): {
    TASK: f"translation",
    MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-dra",
    INITIAL_TOKEN: ">>kan<<",
    SCORE: 2.5
},
"""

"""
(ENGLISH, WELSH): {
    TASK: f"translation",
    MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{WELSH}",
    INITIAL_TOKEN: "",
    SCORE: 1,
},
"""
"""
(ENGLISH, HAUSA): {
    TASK: f"translation",
    MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{HAUSA}",
    INITIAL_TOKEN: "",
    SCORE: 1.5,
},
"""

"""
(ENGLISH, TAMIL): {
    TASK: f"translation",
    MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-dra",
    INITIAL_TOKEN: ">>tam<<",
    SCORE: 3,
},
"""
"""
(ENGLISH, HEBREW): {
    TASK: f"translation",
    MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{HEBREW}",
    INITIAL_TOKEN: "",
    SCORE: 3.5,
},
"""
"""
(SPANISH, YORUBA): {
    TASK: f"translation",
    MODEL: f"Helsinki-NLP/opus-mt-{SPANISH}-{YORUBA}",
    INITIAL_TOKEN: "",
    SCORE: 2.5
},
"""

"""
(ENGLISH, HAITIAN): {
    TASK: f"translation",
    MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{HAITIAN}",
    INITIAL_TOKEN: "",
    SCORE: 2,
},
"""
"""
(ENGLISH, MONGOLIAN): {
    TASK: f"translation",
    MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{MULTIPLE_LANGUAGES}",
    INITIAL_TOKEN: ">>mon<<",
    SCORE: 2,
},
"""
"""
   (ENGLISH, VIETNAMESE): {
       TASK: f"translation",
       MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{VIETNAMESE}",
       INITIAL_TOKEN: "",
       SCORE: 2.5
   },
   """

"""
(ENGLISH, AZERBAIJANI): {
    TASK: f"translation",
    MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{AZERBAIJANI}",
    INITIAL_TOKEN: "",
    SCORE: 1.5,
},
"""
"""
(ENGLISH, GEORGIAN): {
    TASK: f"translation",
    MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{MULTIPLE_LANGUAGES}",
    INITIAL_TOKEN: ">>kat<<",
    SCORE: 2,
},
"""
"""
(ENGLISH, MARATHI): {
    TASK: f"translation",
    MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{MARATHI}",
    INITIAL_TOKEN: "",
    SCORE: 1,
},
"""
"""
(ENGLISH, ROMANIAN): {
    TASK: f"translation",
    MODEL: f"Helsinki-NLP/opus-mt-tc-big-{ENGLISH}-{ROMANIAN}",
    INITIAL_TOKEN: "",
    SCORE: 3,
},
"""

"""
  (ENGLISH, TELUGU): {
      TASK: f"translation",
      MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-dra",
      INITIAL_TOKEN: ">>tel<<",
      SCORE: 3,
  },
  """

"""
    (ENGLISH, URDU): {
        TASK: f"translation",
        MODEL: f"Helsinki-NLP/opus-mt-{ENGLISH}-{URDU}",
        INITIAL_TOKEN: "",
        SCORE: 2.5
    },
    """