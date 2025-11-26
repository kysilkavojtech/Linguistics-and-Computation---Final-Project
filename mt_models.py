# mt_models.py  — using Facebook M2M100 for all language pairs

from typing import List
from transformers import M2M100Tokenizer, M2M100ForConditionalGeneration
import torch
from tqdm import tqdm

# Map your language codes to M2M100 language codes.
# For these languages, they are the same ISO codes.
M2M_LANG_CODES = {
    "tr": "tr",   # Turkish
    "fi": "fi",   # Finnish
    "zh": "zh",   # Chinese
    "vi": "vi",   # Vietnamese
    "es": "es",   # Spanish
    "ru": "ru",   # Russian
}


class MTTranslator:
    def __init__(self, lang_pair: str, device: str = "cpu"):
        """
        lang_pair: e.g. 'en-tr'
        We always assume source = English ('en'), target = the other side.
        """
        src, tgt = lang_pair.split("-")
        if src != "en":
            raise ValueError(f"Expected English as source, got {src}")

        if tgt not in M2M_LANG_CODES:
            raise ValueError(f"No M2M language mapping for target '{tgt}'")

        self.src_lang = "en"
        self.tgt_lang = M2M_LANG_CODES[tgt]

        # Load single multilingual model for all pairs
        model_name = "facebook/m2m100_418M"
        self.tokenizer = M2M100Tokenizer.from_pretrained(model_name)
        self.model = M2M100ForConditionalGeneration.from_pretrained(model_name).to(device)

        self.device = device

    def translate_batch(self, src_texts: List[str], batch_size: int = 8) -> List[str]:
        outputs: List[str] = []
        for i in tqdm(range(0, len(src_texts), batch_size), desc="Translating"):
            batch = src_texts[i: i + batch_size]

            # set the source language
            self.tokenizer.src_lang = self.src_lang

            encoded = self.tokenizer(
                batch,
                return_tensors="pt",
                padding=True,
                truncation=True,
            ).to(self.device)

            generated_tokens = self.model.generate(
                **encoded,
                forced_bos_token_id=self.tokenizer.get_lang_id(self.tgt_lang),
                max_length=128,
            )

            outputs.extend(
                self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
            )

        return outputs
