# build_typology_dataset.py

import os
from typing import List

import torch
import pandas as pd

from config import LANG_CONFIG
from metrics import (
    COMET_MODEL,
    compute_bleu,
    compute_chrf,
    compute_comet,
)

CACHE_DIR = "cache"
OUT_PATH = "data/typology_training_data.csv"

os.makedirs("data", exist_ok=True)


# ---------- basic surface features ----------

def count_tokens(text: str) -> int:
    return len(str(text).strip().split())


def count_chars(text: str) -> int:
    return len(str(text))


def type_token_ratio(text: str) -> float:
    tokens = str(text).strip().split()
    if not tokens:
        return 0.0
    return len(set(tokens)) / len(tokens)


# ---------- COMET sentence-level helper ----------

def compute_sentence_comet(
    src: List[str],
    mt: List[str],
    ref: List[str],
    batch_size: int = 16,
    use_gpu: bool = False,
) -> List[float]:
    """
    Return a list of per-sentence COMET scores aligned with src/mt/ref.
    Uses the already-loaded COMET_MODEL from metrics.py.
    """
    assert len(src) == len(mt) == len(ref)

    data = [{"src": s, "mt": m, "ref": r} for s, m, r in zip(src, mt, ref)]

    result = COMET_MODEL.predict(
        data,
        batch_size=batch_size,
        gpus=1 if use_gpu else 0,
        num_workers=1,
    )

    # Handle different COMET return formats
    if hasattr(result, "scores"):
        seg_scores = result.scores
    elif isinstance(result, dict):
        seg_scores = (
            result.get("scores")
            or result.get("segments_scores")
            or result.get("sentence_scores")
        )
        if seg_scores is None:
            raise ValueError("COMET result dict has no sentence-level scores.")
    else:
        seg_scores, _ = result

    if len(seg_scores) != len(src):
        raise ValueError(
            f"COMET returned {len(seg_scores)} scores for {len(src)} sentences."
        )

    return [float(s) for s in seg_scores]


# ---------- main dataset builder ----------

def build_dataset(
    max_samples: int = 500,
    split: str = "train",
) -> pd.DataFrame:
    """
    Loop over languages in LANG_CONFIG, read cached MT CSVs,
    compute sentence-level features + COMET + corpus-level BLEU/chrF/COMET,
    and return a single big DataFrame.
    """
    rows = []

    use_gpu = torch.cuda.is_available()
    print(f"[INFO] Using GPU for COMET: {use_gpu}")

    for lang_code, cfg in LANG_CONFIG.items():
        pair = cfg["pair"]       # e.g. "en-tr"
        typology = cfg["typology"]

        cache_path = os.path.join(CACHE_DIR, f"{pair}_n{max_samples}_{split}.csv")
        if not os.path.exists(cache_path):
            print(f"[WARN] Cache not found for {pair} at {cache_path} – skipping.")
            continue

        print(f"[INFO] Loading cache for {lang_code} ({pair}) from {cache_path}")
        df = pd.read_csv(cache_path).dropna(subset=["src", "ref", "mt"])

        src_list = df["src"].astype(str).tolist()
        ref_list = df["ref"].astype(str).tolist()
        mt_list  = df["mt"].astype(str).tolist()

        # --- Corpus-level metrics for this language ---
        print(f"[INFO] Computing corpus BLEU/chrF/COMET for {lang_code}")
        bleu_corpus = compute_bleu(mt_list, ref_list)
        chrf_corpus = compute_chrf(mt_list, ref_list)
        comet_corpus = compute_comet(
            src_list,
            mt_list,
            ref_list,
            batch_size=16,
            use_gpu=use_gpu,
        )

        # --- Sentence-level COMET ---
        print(f"[INFO] Computing sentence-level COMET for {lang_code}")
        comet_sentence_scores = compute_sentence_comet(
            src_list,
            mt_list,
            ref_list,
            batch_size=16,
            use_gpu=use_gpu,
        )

        # --- Build rows ---
        for src, ref, mt, comet_sentence in zip(
            src_list, ref_list, mt_list, comet_sentence_scores
        ):
            src_tok = count_tokens(src)
            ref_tok = count_tokens(ref)
            mt_tok  = count_tokens(mt)

            src_char = count_chars(src)
            ref_char = count_chars(ref)
            mt_char  = count_chars(mt)

            len_ratio_mt_src  = mt_tok  / src_tok if src_tok > 0 else 0.0
            len_ratio_ref_src = ref_tok / src_tok if src_tok > 0 else 0.0

            src_cpt = src_char / src_tok if src_tok > 0 else 0.0
            ref_cpt = ref_char / ref_tok if ref_tok > 0 else 0.0
            mt_cpt  = mt_char / mt_tok  if mt_tok  > 0 else 0.0

            src_ttr = type_token_ratio(src)
            ref_ttr = type_token_ratio(ref)
            mt_ttr  = type_token_ratio(mt)

            rows.append({
                "lang": lang_code,
                "pair": pair,
                "typology": typology,
                "src": src,
                "ref": ref,
                "mt": mt,
                # surface features
                "src_len_tokens": src_tok,
                "ref_len_tokens": ref_tok,
                "mt_len_tokens": mt_tok,
                "src_len_chars": src_char,
                "ref_len_chars": ref_char,
                "mt_len_chars": mt_char,
                "len_ratio_mt_src": len_ratio_mt_src,
                "len_ratio_ref_src": len_ratio_ref_src,
                "src_chars_per_token": src_cpt,
                "ref_chars_per_token": ref_cpt,
                "mt_chars_per_token": mt_cpt,
                "src_ttr": src_ttr,
                "ref_ttr": ref_ttr,
                "mt_ttr": mt_ttr,
                # sentence-level COMET
                "comet_sentence": comet_sentence,
                # corpus-level metrics (same for all sentences for this language)
                "bleu_corpus": bleu_corpus,
                "chrf_corpus": chrf_corpus,
                "comet_corpus": comet_corpus,
            })

    big_df = pd.DataFrame(rows)
    print(f"[INFO] Built dataset with shape {big_df.shape}")
    return big_df


def main():
    df = build_dataset(max_samples=500, split="train")
    df.to_csv(OUT_PATH, index=False)
    print(f"[INFO] Saved typology training data to {OUT_PATH}")


if __name__ == "__main__":
    main()
