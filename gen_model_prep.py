# gen_model_prep.py
import random
from typing import List, Dict
from config import MORPHOLOGICAL_LABELS


def make_typology_prompt(
    lang_code: str,
    src_examples: List[str],
    mt_examples: List[str],
    scores: Dict[str, float],
    k: int = 5,
    seed: int = 0,
) -> str:
    """
    Build a prompt for a generative model to guess the morphological typology
    of a language based on MT outputs and system-level scores.

    Lang names are *not* included, so the model only sees text + scores.
    """
    rng = random.Random(seed)
    assert len(src_examples) == len(mt_examples)
    n = len(src_examples)
    k = min(k, n)

    idxs = list(range(n))
    rng.shuffle(idxs)
    idxs = idxs[:k]

    examples_str = ""
    for i in idxs:
        examples_str += (
            f"Source: {src_examples[i]}\nTranslation: {mt_examples[i]}\n\n"
        )

    label_list = ", ".join(MORPHOLOGICAL_LABELS)

    prompt = f"""
You are an expert linguist and machine translation researcher.

Below are {k} examples of English source sentences and their machine translations
into an unknown target language, produced by a strong neural MT system.

You will also see aggregated MT quality scores for this language:
- BLEU: {scores['BLEU']:.2f}
- chrF: {scores['chrF']:.2f}
- COMET: {scores['COMET']:.3f}

Your task: based on these outputs, infer which morphological typology the target
language most likely belongs to.

Possible categories:
{label_list}

Examples:
{examples_str}
Answer with only one word: one of {label_list}.
""".strip()

    return prompt
