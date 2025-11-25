# config.py
"""
Configuration for the MT × Morphological Typology project.

We now use 6 languages and 3 typology groups:
- Agglutinative: Turkish, Finnish
- Isolating: Chinese, Vietnamese
- Fusional: Spanish, Russian
"""

LANG_CONFIG = {
    "tr": {
        "pair": "en-tr",
        "typology": "agglutinative",
        "resource_level": "high",
    },
    "fi": {
        "pair": "en-fi",
        "typology": "agglutinative",
        "resource_level": "medium",
    },
    "zh": {
        "pair": "en-zh",
        "typology": "isolating",
        "resource_level": "high",
    },
    "vi": {
        "pair": "en-vi",
        "typology": "isolating",
        "resource_level": "low",
    },
    "es": {
        "pair": "en-es",
        "typology": "fusional",
        "resource_level": "high",
    },
    "ru": {
        "pair": "en-ru",
        "typology": "fusional",
        "resource_level": "high",
    },
}

# convenience list of possible labels for the generative classifier
MORPHOLOGICAL_LABELS = ["agglutinative", "isolating", "fusional"]
