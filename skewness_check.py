
# Pandas moment skewness (per column)
df[['a', 'b', 'c']].skew()



import pandas as pd
from scipy.stats import skew, skewtest

cols = ['a', 'b', 'c']

# Unbiased skewness (per column)
skew_vals = df[cols].apply(lambda s: skew(s.dropna(), bias=False))

# p-values for H0: skewness == 0 (no skew)
pvals = df[cols].apply(lambda s: skewtest(s.dropna()).pvalue)

print("Skew (unbiased):")
print(skew_vals)
print("\nSkew test p-values (H0: no skew):")
print(pvals)
