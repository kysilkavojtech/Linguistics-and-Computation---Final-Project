# analysis.py
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

"""
Reads mt_typology_results.csv and runs ANOVAs.

We now have 3 groups: agglutinative, isolating, fusional.
No polysynthetic group is included because it wasn't available
in the MT system.
"""

df = pd.read_csv("mt_typology_results.csv")

# encode resource_level as numeric covariate (high=1, medium=0.5, low=0)
resource_map = {"low": 0.0, "medium": 0.5, "high": 1.0}
df["resource_numeric"] = df["resource_level"].map(resource_map)

metrics = ["BLEU", "chrF", "COMET"]

for metric in metrics:
    print("\n" + "=" * 80)
    print(f"ANOVA for {metric}")
    formula = f"{metric} ~ C(typology) + resource_numeric"
    model = ols(formula, data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    print("\nANOVA table:")
    print(anova_table)
    print("\nModel summary:")
    print(model.summary())
