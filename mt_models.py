# mt_models.py
from typing import List, Dict
from tqdm import tqdm
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

"""
MT models for each language pair.
These are OPUS-MT models; you can swap them out for your own system if needed.
Double-check model names on Hugging Face if anything 404s.
"""

MODEL_NAME_FOR_PAIR: Dict[str, str] = {
    "en-tr": "Helsinki-NLP/opus-mt-en-tr",
    "en-fi": "Helsinki-NLP/opus-mt-en-fi",
    "en-zh": "Helsinki-NLP/opus-mt-en-zh",
    "en-vi": "Helsinki-NLP/opus-mt-en-vi",
    "en-es": "Helsinki-NLP/opus-mt-en-es",
    "en-ru": "Helsinki-NLP/opus-mt-en-ru",
}


class MTTranslator:
    def __init__(self, lang_pair: str, device: str = "cpu"):
        if lang_pair not in MODEL_NAME_FOR_PAIR:
            raise ValueError(f"No model mapping found for pair {lang_pair}")

        model_name = MODEL_NAME_FOR_PAIR[lang_pair]
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
        self.device = device

    def translate_batch(self, src_texts: List[str], batch_size: int = 16) -> List[str]:
        outputs: List[str] = []
        for i in tqdm(range(0, len(src_texts), batch_size), desc="Translating"):
            batch = src_texts[i : i + batch_size]
            inputs = self.tokenizer(
                batch, return_tensors="pt", padding=True, truncation=True
            ).to(self.device)
            with torch.no_grad():
                generated = self.model.generate(**inputs, max_length=128)
            outputs.extend(
                self.tokenizer.batch_decode(generated, skip_special_tokens=True)
            )
        return outputs
