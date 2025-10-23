import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Columns containing reliability percentages
reliability_cols = [
    'Annual Leave Reliability',
    'Long Service Leave Reliability',
    'Wages Reliability'
]

# --- 1️⃣ Clean: strip %, convert to float 0–1 scale ---
for col in reliability_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace('%', '', regex=False)
        .str.strip()
        .replace('', np.nan)
        .astype(float)
    ) / 100.0

# --- 2️⃣ Remove outliers (bottom 2.5%, top 97.5%) ---
for col in reliability_cols:
    low, high = df[col].quantile([0.025, 0.975])
    df = df[(df[col] >= low) & (df[col] <= high)]

# --- 3️⃣ Clean missing or invalid data ---
df = df.dropna(subset=reliability_cols)

# --- 4️⃣ Categorise reliability (threshold 95%) ---
threshold = 0.95
df['unreliable_flag'] = (
    (df['Annual Leave Reliability'] < threshold) |
    (df['Long Service Leave Reliability'] < threshold) |
    (df['Wages Reliability'] < threshold)
).astype(int)

# --- 5️⃣ Check class balance ---
class_balance = df['unreliable_flag'].value_counts(normalize=True) * 100
print("Class balance (%):\n", class_balance.round(2))

# Optional quick bar plot
df['unreliable_flag'].value_counts().plot(kind='bar', title='Reliable vs Unreliable')
plt.show()
