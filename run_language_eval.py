import os
import pandas as pd
import torch
from config import LANG_CONFIG
from data_loading import load_opus100_pair
from mt_models import MTTranslator
from metrics import compute_bleu, compute_chrf, compute_comet

def evaluate_language(
    lang_code: str,
    max_samples: int = 5000,
    split: str = "train",
    device: str = None,
) -> dict:
    cfg = LANG_CONFIG[lang_code]
    pair = cfg["pair"]  # e.g. "en-tr"

    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    # --- 1. Define cache path ---
    cache_path = os.path.join("cache", f"{pair}_n{max_samples}_{split}.csv")

    # --- 2. If cached translations exist, load them ---
    if os.path.exists(cache_path):
        print(f"Loading cached translations from {cache_path} ...")
        df_cache = pd.read_csv(cache_path)
        src_texts = df_cache["src"].tolist()
        ref_texts = df_cache["ref"].tolist()
        mt_texts  = df_cache["mt"].tolist()
    else:
        # --- 3. Otherwise, load data + run MT and cache it ---
        print(f"Loading data for {pair} (split={split}, max_samples={max_samples})...")
        src_texts, ref_texts = load_opus100_pair(
            pair, split=split, max_samples=max_samples, seed=42
        )

        print(f"Running MT for {pair} on device={device} ...")
        translator = MTTranslator(pair, device=device)
        mt_texts = translator.translate_batch(src_texts, batch_size=8)

        # Save to cache
        df_cache = pd.DataFrame({
            "src": src_texts,
            "ref": ref_texts,
            "mt": mt_texts,
        })
        df_cache.to_csv(cache_path, index=False)
        print(f"Saved cached translations to {cache_path}")

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