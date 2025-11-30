# make_unseen_mystery_corpora.py -- Preliminary testing helper

import os
import pandas as pd
from data_loading import load_opus100_pair

OUT_DIR = "mystery_corpora_unseen"
os.makedirs(OUT_DIR, exist_ok=True)

# Random mystery languages for testing:
MYSTERY_PAIRS = {
    "kk": "en-kk",  # Kazakh  (agglutinative)
    "ha": "en-ha",  # Hausa   (analytic / isolating-leaning)
    "cs": "cs-en",  # Czech   (fusional)
}

def make_mystery_corpus(
    lang_code: str,
    pair: str,
    split: str = "test",
    max_samples: int = 500,
    seed: int = 123,
):
    print(f"[INFO] Building mystery corpus for {lang_code} (pair={pair})...")
    src_texts, ref_texts = load_opus100_pair(
        pair, split=split, max_samples=max_samples, seed=seed
    )

    src_lang, tgt_lang = pair.split("-")

    # Ensure English is the source side
    if src_lang != "en":
        src_texts, ref_texts = ref_texts, src_texts

    df = pd.DataFrame({
        "en": src_texts,
        "unk": ref_texts,
    })

    out_path = os.path.join(OUT_DIR, f"mystery_{lang_code}.csv")
    df.to_csv(out_path, index=False)
    print(f"[INFO] Saved to {out_path} (n={len(df)})")

def main():
    for code, pair in MYSTERY_PAIRS.items():
        make_mystery_corpus(code, pair)

if __name__ == "__main__":
    main()
