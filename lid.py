# lid.py
import fasttext
from functools import lru_cache
from collections import Counter

LID_MODEL_PATH = "models/lid.176.bin"

@lru_cache(maxsize=1)
def get_lid_model():
    return fasttext.load_model(LID_MODEL_PATH)

def detect_lang(text: str):
    model = get_lid_model()
    cleaned = str(text).replace("\n", " ").strip()
    labels, probs = model.predict(cleaned, k=1)
    lang = labels[0].replace("__label__", "")
    return lang, float(probs[0])

def majority_lang(texts, min_conf: float = 0.7):
    """
    Detect language for many sentences; return majority fastText code + stats.
    """
    counts = Counter()
    confs = []

    for t in texts:
        lang, conf = detect_lang(t)
        if conf >= min_conf:
            counts[lang] += 1
            confs.append(conf)

    if not counts:
        # TODO: Add option to manually add
        raise ValueError("No high-confidence LID predictions.")

    most_common_lang, n = counts.most_common(1)[0]
    return {
        "ft_lang": most_common_lang,
        "n_high_conf": n,
        "avg_conf": sum(confs) / len(confs),
        "dist": dict(counts),
    }
