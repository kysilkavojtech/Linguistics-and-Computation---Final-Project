Morphological Typology and Machine Translation Quality
Victoria Duran-Valero, Vojtech Kysilka, Ali Otuzoglu

For our project, the research question we hope to investigate is whether the quality of Machine Translation (MT) differs significantly across languages with varying levels of morphological richness, specifically across agglutinative, isolating, fusional, and polysynthetic languages. We want to examine whether MT performance shows a group effect based on these morphological categories and whether generative models can accurately predict morphological typology from translation outputs.
We will use state-of-the-art MT algorithms along with parallel language corpora from OPUS-100 (English‑centric corpus covering 100 languages), which provides coverage of the different morphological types with the hopes of comparing translation performance across groups.
To evaluate differences across groups, we will use a one‑way ANOVA model to test for statistically significant effects of typology category on translation quality metrics, for example BLEU, chrF, COMET. We will also implement a generative model based on Freitag et al. (2023). We would adjust with a normalizing variable for low‑resource vs high‑resource languages to account for more common and less common languages. We have a couple simplifying assumptions. Firstly, we will be limiting the analysis to 1-2 languages per typology group, using the OPUS‑100 corpora exclusively with English as one language side. We are also assuming that the groupings agglutinative, isolating, fusional, polysynthetic can be treated as discrete categories. We will use the classifications from past studies to assign each language to a typology group.
In terms of results, we will evaluate using an alpha of 0.05 for statistical significance. We will also test our generative model using anonymized language groups to assess its accuracy, building on other works in MT evaluation (see references).

References
- https://direct.mit.edu/coli/article/51/1/73/124465/Machine-Translation-Meta-Evaluation-through
- https://aclanthology.org/2023.wmt-1.51.pdf
- https://arxiv.org/pdf/2404.11553

