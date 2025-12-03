How to use

Step 0 — Install dependencies

1. (Optional) Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Importantly, the `comet` library does not work reliably in newer versions of Python. `python 3.10` was used in building this project.

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Download the fastText language-identification model (required by some scripts):

```bash
mkdir -p models
cd models
curl -O https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
cd ..
```

Step 1 — Generate cache files and run MT evaluation

**Important:** This step must be run before building the training dataset.

```bash
python run_language_eval.py
```

This script:
- Loads parallel corpora from OPUS-100 for each language in `config.py`
- Runs machine translation using M2M100
- Computes BLEU, chrF, and COMET metrics
- Saves cached translations to `cache/` directory (e.g., `cache/en-tr_n500_train.csv`)
- Outputs: `mt_typology_results.csv` with evaluation results

**Note:** This step can take significant time depending on your hardware (GPU recommended).

Step 2 — Build training data (one-time)

**Prerequisite:** Step 1 must be completed first (cache files must exist).

```bash
python build_typology_dataset.py
```

This script:
- Reads cached MT outputs from `cache/` directory
- Computes sentence-level features (token counts, chars per token, TTR, etc.)
- Computes sentence-level COMET scores
- Generates: `data/typology_training_data.csv`

Step 3 — Train the typology classifier

**Prerequisite:** Step 2 must be completed first (`data/typology_training_data.csv` must exist).

```bash
python train_typology_classifier.py
```

Outputs:
- `models/typology_clf.joblib`
- Console: accuracy, classification report, confusion matrix

Step 4 (Optional) — Generate test corpora (for testing purposes if the user wants to try Step 5 based on OPUS-100 data)

```bash
python make_unseen_mystery_corpora.py
```

Creates files in `mystery_corpora_unseen/`, e.g.:
- `mystery_corpora_unseen/mystery_kk.csv` (agglutinative)
- `mystery_corpora_unseen/mystery_cs.csv` (fusional)

Each file contains ~500 English / unknown-language sentence pairs.

Step 5 — Predict typology for a mystery corpus

**Prerequisite:** Step 3 must be completed first (`models/typology_clf.joblib` must exist).

1. Edit `classifier_runner.py` so the data-loading line points to the desired file. Example:

```python
df = pd.read_csv("mystery_corpora_unseen/mystery_cs.csv")
```

2. Run the script:

```bash
python classifier_runner.py
```

Example output (2 real runs):

```
fastText majority: cs
BLEU: 19.45
chrF: 40.64
COMET: 0.75

Predicted typology (majority vote): fusional
Predicted typology (prob avg): fusional (p=0.912)
Class-wise avg probs:
  agglutinative: 0.012
  fusional: 0.912
  isolating: 0.076
```

```
fastText majority: kk
BLEU: 2.41
chrF: 9.42
COMET: 0.58

Predicted typology (majority vote): agglutinative
Predicted typology (prob avg): agglutinative (p=0.728)
Class-wise avg probs:
  agglutinative: 0.727
  fusional: 0.000
  isolating: 0.273
```