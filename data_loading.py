# data_loading.py
from datasets import load_dataset
from typing import List, Tuple
import random


def load_opus100_pair(
    lang_pair: str,
    split: str = "train",
    max_samples: int = 2000,
    seed: int = 42,
) -> Tuple[List[str], List[str]]:
    """
    Load parallel sentences from OPUS-100 for a given language pair.

    Args:
        lang_pair: e.g. "en-tr"
        split: dataset split ("train", "validation", "test")
        max_samples: maximum number of sentence pairs to keep
        seed: random seed for sampling

    Returns:
        src_texts (English), ref_texts (target language)
    """
    ds = load_dataset("Helsinki-NLP/opus-100", lang_pair, split=split)

    src_lang, tgt_lang = lang_pair.split("-")

    indices = list(range(len(ds)))
    random.Random(seed).shuffle(indices)
    indices = indices[:max_samples]

    src_texts = []
    ref_texts = []
    for i in indices:
        item = ds[i]["translation"]
        src_texts.append(item[src_lang])
        ref_texts.append(item[tgt_lang])

    return src_texts, ref_texts
