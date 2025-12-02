import pandas as pd
from lid import majority_lang

df = pd.read_csv("mystery_corpora_unseen/mystery_kk.csv")  # columns: 'en', 'unk'

# Clean data: drop rows with NaN and ensure strings
df = df.dropna(subset=["en", "unk"])
df["en"] = df["en"].astype(str)
df["unk"] = df["unk"].astype(str)

en_texts = df["en"].tolist()
unk_texts = df["unk"].tolist()

lid_info = majority_lang(unk_texts, min_conf=0.7)
m2m_lang = lid_info["ft_lang"]

print("fastText majority:", m2m_lang)
print("LID stats:", lid_info)

# -----------------------

from mt_models import MTTranslator

pair = f"en-{m2m_lang}"
translator = MTTranslator(pair, device="cpu")

mt_texts = translator.translate_batch(en_texts, batch_size=8)

# -----------------------

from metrics import compute_bleu, compute_chrf, compute_comet

bleu = compute_bleu(mt_texts, unk_texts)
chrf = compute_chrf(mt_texts, unk_texts)
comet = compute_comet(
    en_texts,
    mt_texts,
    unk_texts,
    batch_size=16,
    use_gpu=True,   # or False, depending on your setup
)

print("BLEU:", bleu)
print("chrF:", chrf)
print("COMET:", comet)

import torch
from build_typology_dataset import compute_sentence_comet

use_gpu = torch.cuda.is_available()

comet_sentence_scores = compute_sentence_comet(
    en_texts,
    mt_texts,
    unk_texts,
    batch_size=16,
    use_gpu=use_gpu,
)


# ------------------------

import pandas as pd
from build_typology_dataset import count_tokens, count_chars, type_token_ratio

rows = []
for src, ref, mt, comet_sentence in zip(en_texts, unk_texts, mt_texts, comet_sentence_scores):
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
        # NEW: sentence-level COMET
        "comet_sentence": comet_sentence,
        # NEW: corpus-level metrics (same for every sentence)
        "bleu_corpus": bleu,
        "chrf_corpus": chrf,
        "comet_corpus": comet,
    })

mystery_df = pd.DataFrame(rows)

# ------------------------

import joblib

feature_cols = [
    "src_len_tokens",
    "ref_len_tokens",
    "mt_len_tokens",
    "src_len_chars",
    "ref_len_chars",
    "mt_len_chars",
    "len_ratio_mt_src",
    "len_ratio_ref_src",
    "src_chars_per_token",
    "ref_chars_per_token",
    "mt_chars_per_token",
    "src_ttr",
    "ref_ttr",
    "mt_ttr",
    "comet_sentence",
    "bleu_corpus",
    "chrf_corpus",
    "comet_corpus",
]


clf = joblib.load("models/typology_clf.joblib")

X_mystery = mystery_df[feature_cols]
y_pred = clf.predict(X_mystery)           # per sentence
probs = clf.predict_proba(X_mystery)      # per sentence, class probabilities
classes = clf.classes_

# -------------------

import numpy as np
from collections import Counter

# Majority vote over sentence-level predictions
count = Counter(y_pred)
pred_typology_majority = count.most_common(1)[0][0]

# Optionally, average probabilities to get a softer global prediction
avg_probs = probs.mean(axis=0)
global_pred_idx = int(np.argmax(avg_probs))
pred_typology_prob = classes[global_pred_idx]
confidence = avg_probs[global_pred_idx]

print("Predicted typology (majority vote):", pred_typology_majority)
print("Predicted typology (prob avg):", pred_typology_prob, f"(p={confidence:.3f})")
print("Class-wise avg probs:")
for c, p in zip(classes, avg_probs):
    print(f"  {c}: {p:.3f}")

