# run_language_eval.py
import torch
import pandas as pd
from typing import Dict, Any

from config import LANG_CONFIG
from data_loading import load_opus100_pair
from mt_models import MTTranslator
from metrics import compute_bleu, compute_chrf, compute_comet


def evaluate_language(
    lang_code: str,
    max_samples: int = 2000,
    split: str = "train",
    device: str = None,
) -> Dict[str, Any]:
    """
    Run MT + metrics for a single target language.

    Returns a dict suitable for putting into a DataFrame row.
    """
    cfg = LANG_CONFIG[lang_code]
    pair = cfg["pair"]  # e.g. "en-tr"

    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"Loading data for {pair} (split={split}, max_samples={max_samples})...")
    src_texts, ref_texts = load_opus100_pair(pair, split=split, max_samples=max_samples)

    print(f"Running MT for {pair} on device={device} ...")
    translator = MTTranslator(pair, device=device)
    mt_texts = translator.translate_batch(src_texts, batch_size=16)

    print("Computing BLEU / chrF / COMET ...")
    bleu = compute_bleu(mt_texts, ref_texts)
    chrf = compute_chrf(mt_texts, ref_texts)
    comet = compute_comet(
        src_texts,
        mt_texts,
        ref_texts,
        batch_size=16,
        use_gpu=device.startswith("cuda"),
    )

    return {
        "language": lang_code,
        "pair": pair,
        "typology": cfg["typology"],
        "resource_level": cfg["resource_level"],
        "BLEU": bleu,
        "chrF": chrf,
        "COMET": comet,
        "n_samples": len(src_texts),
    }


def main():
    rows = []
    for lang in LANG_CONFIG.keys():
        print("=" * 60)
        print(f"Evaluating language: {lang}")
        row = evaluate_language(lang)
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv("mt_typology_results.csv", index=False)
    print("\nFinal results:")
    print(df)


if __name__ == "__main__":
    main()
