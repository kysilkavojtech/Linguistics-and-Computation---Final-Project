# train_typology_classifier.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import joblib

DATA_PATH = "data/typology_training_data.csv"
MODEL_PATH = "models/typology_clf.joblib"


def main():
    print(f"[INFO] Loading data from {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)

    # ---- define feature columns ----
    feature_cols = [
        # surface / length features
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
        # sentence-level COMET
        "comet_sentence",
        # corpus-level metrics (same for all sentences in a language)
        "bleu_corpus",
        "chrf_corpus",
        "comet_corpus",
    ]

    # drop rows with missing features / labels
    df = df.dropna(subset=feature_cols + ["typology"])
    print(f"[INFO] Dataset after dropna: {df.shape}")

    X = df[feature_cols]
    y = df["typology"]  # "agglutinative", "fusional", "isolating"

    # ---- train/test split ----
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.1,
        random_state=42,
        stratify=y,  # keep class balance
    )

    print(f"[INFO] Train size: {X_train.shape}, Test size: {X_test.shape}")

    # ---- model: StandardScaler + multinomial logistic regression ----
    clf = make_pipeline(
        StandardScaler(),
        LogisticRegression(
            max_iter=1000,
            multi_class="multinomial",
            n_jobs=-1,
        ),
    )

    print("[INFO] Training classifier...")
    clf.fit(X_train, y_train)

    # ---- evaluation ----
    y_pred = clf.predict(X_test)
    print("=== Classification report ===")
    print(classification_report(y_test, y_pred))

    labels = ["agglutinative", "fusional", "isolating"]
    print("=== Confusion matrix (rows=true, cols=pred) ===")
    print(confusion_matrix(y_test, y_pred, labels=labels))

    # ---- save model ----
    os.makedirs("models", exist_ok=True)
    joblib.dump(clf, MODEL_PATH)
    print(f"[INFO] Saved trained classifier to {MODEL_PATH}")


if __name__ == "__main__":
    import os
    main()
