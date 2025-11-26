# Overview of MT Evaluation Metrics: BLEU, chrF, and COMET

Machine Translation (MT) quality can be evaluated through a variety of metrics, each designed to capture different aspects of translation accuracy, fluency, and semantic fidelity. This write-up explains how three widely used metrics—**BLEU**, **chrF**, and **COMET**—operate and what they are intended to measure.

---

## 1. BLEU (Bilingual Evaluation Understudy)

### **What BLEU Measures**
BLEU evaluates **n-gram overlap** between a system-generated translation (the *candidate*) and one or more human translations (the *references*). It is designed to approximate how similar the MT output is to human-produced text.

### **How BLEU Works**
1. **N-gram precision**:  
   - BLEU counts how many n-grams (typically 1–4 grams) in the candidate also appear in the reference.
   - This is a *precision-based* metric, meaning it measures *how much of the candidate is correct*.

2. **Clipping**:  
   - BLEU prevents inflated scores by **clipping** counts of repeated n-grams.  
   - If the candidate repeats a word more times than the reference, extra occurrences do not contribute.

3. **Brevity Penalty (BP)**:
   - A penalty to prevent short candidates from unfairly scoring high.  
   - If the candidate is shorter than the reference, BP < 1.

4. **Final Score**:
   - BLEU combines geometric averages of n-gram precisions with the brevity penalty.

### **Strengths**
- Fast and easy to compute.
- Reasonably correlates with human judgments at the corpus level.

### **Limitations**
- Sensitive to surface form differences.  
- Struggles with morphologically rich languages because exact n-gram matches drop sharply.  
- Does not measure semantic adequacy.

---

## 2. chrF (Character F-score)

### **What chrF Measures**
chrF evaluates translation quality using **character-level n-gram precision and recall**, producing an F-score. It measures how similar the candidate and reference are in terms of character sequences, making it more robust to morphological variation.

### **How chrF Works**
1. **Character n-grams** (usually 1–6) are extracted from both the candidate and reference.
2. **Precision (P)**: proportion of candidate n-grams found in the reference.  
3. **Recall (R)**: proportion of reference n-grams found in the candidate.  
4. **F-score** combines precision and recall, usually with β = 2 to weight recall more heavily.

chrF also has a variant, **chrF++**, which incorporates some word-level n-grams in addition to character-level ones.

### **Strengths**
- Performs well across typologically diverse languages.  
- Less affected by inflectional differences or word segmentation issues.  
- Symmetric treatment of under- and over-translation.

### **Limitations**
- Does not directly measure semantics.  
- Still based on surface similarity, though at a finer granularity.

---

## 3. COMET (Crosslingual Optimized Metric for Evaluation of Translation)

### **What COMET Measures**
COMET predicts MT quality using **neural network models** trained to approximate **human judgments**. It uses contextual embeddings to measure **semantic similarity** between source, candidate, and reference.

### **How COMET Works**
Although there are several variants (e.g., COMET-QE, COMET-22), most COMET models use the following framework:

1. Input representations:
   - The *source sentence*
   - The *candidate translation*
   - The *reference translation* (except in QE variants)

2. **Neural Encoder**:
   - Uses pretrained language models such as XLM-R or mBERT to produce contextual embeddings.

3. **Scoring Model / Regression Head**:
   - The system is trained on datasets where humans assigned quality scores (e.g., MQM or DA scores).
   - The model learns to predict a continuous quality score that correlates with human preferences.

### **Strengths**
- Captures **semantic adequacy** better than n-gram metrics.  
- Strong correlations with human evaluators across languages and tasks.  
- Can account for paraphrasing and morphological variation.

### **Limitations**
- Requires significant computational resources.  
- Dependent on training data and may be biased by evaluator distributions.  
- Less transparent and harder to interpret than n-gram scores.

---

## Summary Table

| Metric | Level | Measures | Best For | Weaknesses |
|-------|--------|-----------|-----------|--------------|
| **BLEU** | Word / n-gram | Precision of n-gram overlap | High-resource languages, large corpora | Poor for morphology-rich languages; no semantics |
| **chrF** | Character | F-score of character-level similarity | Diverse morphologies, under-/over-segmentation issues | Still surface-level; no inherent semantic modeling |
| **COMET** | Semantic / neural | Learned quality estimation aligned with human judgments | Semantic adequacy, paraphrases, cross-lingual meaning | Requires heavy models; less interpretable |

---

If you want, I can turn this into a PDF, integrate it into your original write-up, or expand it into slides for a presentation.
