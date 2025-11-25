# metrics.py
from typing import List, Tuple
import sacrebleu
from comet import download_model, load_from_checkpoint

# load COMET once and reuse
COMET_MODEL_PATH = download_model("Unbabel/wmt22-comet-da")
COMET_MODEL = load_from_checkpoint(COMET_MODEL_PATH)


def compute_bleu(system_outputs: List[str], references: List[str]) -> float:
    bleu = sacrebleu.corpus_bleu(system_outputs, [references])
    return float(bleu.score)


def compute_chrf(system_outputs: List[str], references: List[str]) -> float:
    chrf = sacrebleu.corpus_chrf(system_outputs, [references])
    return float(chrf.score)


def compute_comet(
    src: List[str],
    mt: List[str],
    ref: List[str],
    batch_size: int = 16,
    use_gpu: bool = False,
) -> float:
    data = [{"src": s, "mt": m, "ref": r} for s, m, r in zip(src, mt, ref)]
    gpus = 1 if use_gpu else 0
    seg_scores, sys_score = COMET_MODEL.predict(
        data, batch_size=batch_size, gpus=gpus
    )
    return float(sys_score)
