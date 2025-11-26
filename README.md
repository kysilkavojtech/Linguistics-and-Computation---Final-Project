# Morphological Typology and Machine Translation Quality  
**Victoria Duran-Valero, Vojtech Kysilka, Ali Otuzoglu**

## Research Question  
Our project investigates whether the quality of Machine Translation (MT) differs significantly across languages with varying levels of morphological richness—specifically **agglutinative**, **isolating**, **fusional**, and **polysynthetic** languages. We aim to determine:

1. Whether MT performance shows a **group-level effect** based on these morphological categories.  
2. Whether a **generative model** can accurately infer morphological typology from translation outputs.

## Data and Methods  

### **Datasets**  
We use parallel language corpora from **OPUS-100**, an English-centric dataset covering 100 languages. This corpus provides representation across all major morphological types, allowing group-level comparisons.

### **Machine Translation Systems**  
We will test translation quality using **state-of-the-art MT algorithms**, keeping English as the source or target language for consistency.

### **Evaluation Metrics**  
Translation performance will be assessed using widely adopted MT metrics:  
- **BLEU**  
- **chrF**  
- **COMET**

### **Statistical Analysis**  
To examine group differences, we will run a **one-way ANOVA** to test whether morphological typology significantly affects MT quality.  
We will also include a **normalizing variable** to control for differences between high-resource and low-resource languages.

### **Generative Model Approach**  
Following Freitag et al. (2023), we will implement a generative model to predict typology based on translation outputs. Languages will be anonymized to ensure unbiased predictions.

## Assumptions and Limitations  
- We limit language selection to **1–2 languages per typology group**.  
- We rely exclusively on **OPUS-100** with **English** as one side of each language pair.  
- We treat typological categories as **discrete**, even though linguistic typology exists on a spectrum.  
- Language classifications follow prior published studies.

## Expected Outcomes  
- Statistical significance will be evaluated at **α = 0.05**.  
- We will assess the generative model's accuracy in reconstructing typology categories.  
- Findings will contribute to understanding how morphological complexity interacts with MT performance.

## References  
- <https://direct.mit.edu/coli/article/51/1/73/124465/Machine-Translation-Meta-Evaluation-through>  
- <https://aclanthology.org/2023.wmt-1.51.pdf>  
- <https://arxiv.org/pdf/2404.11553>
