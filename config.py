# config.py
"""
24-language high-resource typology configuration
8 languages per group:
- agglutinative
- isolating
- fusional
"""

LANG_CONFIG = {

    # ---------------------------------------------------------
    # AGGLUTINATIVE LANGUAGES (8)
    # ---------------------------------------------------------

    # Turkish — classic agglutinative morphology
    # Source: Johanson & Csató (1998), The Turkic Languages
    # https://wals.info/languoid/lect/wals_code_tur
    "tr": {"name": "Turkish", "pair": "en-tr",
           "typology": "agglutinative", "resource_level": "high"},

    # Finnish — Uralic, strongly agglutinative
    # Source: Karlsson (1999), Finnish Grammar
    # https://wals.info/languoid/lect/wals_code_fin
    "fi": {"name": "Finnish", "pair": "en-fi",
           "typology": "agglutinative", "resource_level": "medium"},

    # Hungarian — Uralic, strongly agglutinative
    # Source: É. Kiss (2002), The Syntax of Hungarian
    # https://wals.info/languoid/lect/wals_code_hun
    "hu": {"name": "Hungarian", "pair": "en-hu",
           "typology": "agglutinative", "resource_level": "medium"},

    # Korean — classic agglutinative structure
    # Source: Sohn (1999), Korean
    # https://wals.info/languoid/lect/wals_code_kor
    "ko": {"name": "Korean", "pair": "en-ko",
           "typology": "agglutinative", "resource_level": "high"},

    # Japanese — textbook example of agglutination
    # Source: Shibatani (1990), Japanese
    # https://wals.info/languoid/lect/wals_code_jpn
    "ja": {"name": "Japanese", "pair": "en-ja",
           "typology": "agglutinative", "resource_level": "high"},

    # Tamil — Dravidian languages are strongly agglutinative
    # Source: Steever (1998), The Dravidian Languages
    # https://wals.info/languoid/lect/wals_code_tam
    "ta": {"name": "Tamil", "pair": "en-ta",
           "typology": "agglutinative", "resource_level": "medium"},

    # Kannada — Dravidian, strongly agglutinative
    # Source: Schiffman (2000), A Grammar of Spoken Kannada
    # https://wals.info/languoid/lect/wals_code_kan
    "kn": {"name": "Kannada", "pair": "en-kn",
           "typology": "agglutinative", "resource_level": "low"},

    # Mongolian — Altaic/Mongolic agglutinative
    # Source: Janhunen (2012), Mongolian
    # https://wals.info/languoid/lect/wals_code_mon
    "mn": {"name": "Mongolian", "pair": "en-mn",
           "typology": "agglutinative", "resource_level": "low"},

    # ---------------------------------------------------------
    # ISOLATING LANGUAGES (8)
    # ---------------------------------------------------------

    # Chinese — prototypical isolating language
    # Source: Comrie (1981), Typology
    # https://wals.info/languoid/lect/wals_code_mnd
    "zh": {"name": "Chinese", "pair": "en-zh",
           "typology": "isolating", "resource_level": "high"},

    # Vietnamese — textbook isolating/analytic morphology
    # Source: Thompson (1987), Vietnamese
    # https://wals.info/languoid/lect/wals_code_vie
    "vi": {"name": "Vietnamese", "pair": "en-vi",
           "typology": "isolating", "resource_level": "medium"},

    # Thai — isolating Tai-Kadai language
    # Source: Enfield (2005)
    # https://wals.info/languoid/lect/wals_code_tha
    "th": {"name": "Thai", "pair": "en-th",
           "typology": "isolating", "resource_level": "medium"},

    # Malay — low-synthesis analytic morphology
    # Source: Sneddon (2010), Malay Grammar
    # https://wals.info/languoid/lect/wals_code_mly
    "ms": {"name": "Malay", "pair": "en-ms",
           "typology": "isolating", "resource_level": "medium"},

    # Indonesian — analytic morphology
    # Source: Sneddon (2010), Indonesian Grammar
    # https://wals.info/languoid/lect/wals_code_ind
    "id": {"name": "Indonesian", "pair": "en-id",
           "typology": "isolating", "resource_level": "high"},

    # Khmer — classical isolating language
    # Source: Huffman (1970)
    # https://wals.info/languoid/lect/wals_code_khm
    "km": {"name": "Khmer", "pair": "en-km",
           "typology": "isolating", "resource_level": "low"},

    # Burmese — Sino-Tibetan isolating morphology
    # Source: Watkins (2001)
    # https://wals.info/languoid/lect/wals_code_brm
    "my": {"name": "Burmese", "pair": "en-my",
           "typology": "isolating", "resource_level": "low"},

    # Yoruba — analytic low-inflection morphology
    # Source: Bamgbose (1966), Yoruba Grammar
    # https://wals.info/languoid/lect/wals_code_yor
    "yo": {"name": "Yoruba", "pair": "en-yo",
           "typology": "isolating", "resource_level": "low"},

    # ---------------------------------------------------------
    # FUSIONAL LANGUAGES (8)
    # ---------------------------------------------------------

    # Spanish — Romance languages = fusional
    # Source: Harris (1988)
    # https://wals.info/languoid/lect/wals_code_spa
    "es": {"name": "Spanish", "pair": "en-es",
           "typology": "fusional", "resource_level": "high"},

    # French — Romance fusional morphology
    # Source: Grevisse (1993)
    # https://wals.info/languoid/lect/wals_code_fre
    "fr": {"name": "French", "pair": "en-fr",
           "typology": "fusional", "resource_level": "high"},

    # German — Indo-European fusional morphology
    # Source: Duden Grammar
    # https://wals.info/languoid/lect/wals_code_ger
    "de": {"name": "German", "pair": "de-en",
           "typology": "fusional", "resource_level": "high"},

    # Russian — Slavic fusional
    # Source: Corbett (2008)
    # https://wals.info/languoid/lect/wals_code_rus
    "ru": {"name": "Russian", "pair": "en-ru",
           "typology": "fusional", "resource_level": "high"},

    # Portuguese — Romance fusional
    # Source: Maiden (1995)
    # https://wals.info/languoid/lect/wals_code_por
    "pt": {"name": "Portuguese", "pair": "en-pt",
           "typology": "fusional", "resource_level": "high"},

    # Italian — Romance fusional
    # Source: Maiden (1995)
    # https://wals.info/languoid/lect/wals_code_ita
    "it": {"name": "Italian", "pair": "en-it",
           "typology": "fusional", "resource_level": "high"},

    # Polish — Slavic fusional morphology
    # Source: Swan (2002)
    # https://wals.info/languoid/lect/wals_code_pol
    "pl": {"name": "Polish", "pair": "en-pl",
           "typology": "fusional", "resource_level": "medium"},

    # Dutch — Germanic fusional
    # Source: Donaldson (1997)
    # https://wals.info/languoid/lect/wals_code_nld
    "nl": {"name": "Dutch", "pair": "en-nl",
           "typology": "fusional", "resource_level": "medium"},
}

# Convenience lists
ALL_LANG_CODES = list(LANG_CONFIG.keys())

AGGLUTINATIVE_LANGS = [c for c, d in LANG_CONFIG.items() if d["typology"] == "agglutinative"]
ISOLATING_LANGS     = [c for c, d in LANG_CONFIG.items() if d["typology"] == "isolating"]
FUSIONAL_LANGS      = [c for c, d in LANG_CONFIG.items() if d["typology"] == "fusional"]
