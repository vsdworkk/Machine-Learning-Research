import pandas as pd
import numpy as np

# List of reliability columns
reliability_cols = [
    'Annual Leave Reliability',
    'Long Service Leave Reliability',
    'Wages Reliability'
]

# --- 1️⃣ Remove outliers (bottom 2.5% / top 97.5%) ---
for col in reliability_cols:
    lower = df[col].quantile(0.025)
    upper = df[col].quantile(0.975)
    df = df[(df[col] >= lower) & (df[col] <= upper)]

# --- 2️⃣ Clean data before categorisation ---
# Drop rows with any missing or non-numeric values in reliability cols
df = df.dropna(subset=reliability_cols)

# Ensure numeric type
for col in reliability_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# --- 3️⃣ Create reliability flag ---
threshold = 0.95
df['unreliable_flag'] = (
    (df['Annual Leave Reliability'] < threshold) |
    (df['Long Service Leave Reliability'] < threshold) |
    (df['Wages Reliability'] < threshold)
).astype(int)

# --- 4️⃣ Check class balance ---
class_balance = df['unreliable_flag'].value_counts(normalize=True) * 100
print("Class balance (%):\n", class_balance.round(2))

# Optional: visual check
import matplotlib.pyplot as plt
df['unreliable_flag'].value_counts().plot(kind='bar', title='Reliable vs Unreliable Cases')
plt.show()
