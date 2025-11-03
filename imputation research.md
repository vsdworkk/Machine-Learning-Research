

```

## Decision Tree Summary
```
Is the variable NUMERICAL?
│
├─ YES
│  │
│  ├─ Is it highly skewed (|skewness| > 1)?
│  │  ├─ YES → Use MEDIAN
│  │  └─ NO → Check outliers
│  │         ├─ Many outliers → Use MEDIAN
│  │         └─ Few outliers → Use MEAN
│  │
│  └─ Few unique values (<10)?
│     └─ YES → Use MODE (treat as categorical)
│
└─ NO (Categorical)
   │
   ├─ High cardinality (>50 unique)?
   │  └─ YES → Use 'Missing' or 'Unknown' constant
   │
   └─ Low cardinality
      └─ Use MODE (most frequent)



def recommended_imputation(df):
    """
    Simple, practical imputation strategy
    """
    df_imputed = df.copy()
    
    for col in df.columns:
        if df[col].isna().sum() > 0:
            # Always add indicator
            df_imputed[f'{col}_missing'] = df[col].isna().astype(int)
            
            # Numerical: always use median (robust to outliers and skewness)
            if df[col].dtype in ['float64', 'int64']:
                df_imputed[col].fillna(df[col].median(), inplace=True)
            
            # Categorical: always use mode
            else:
                mode_val = df[col].mode()[0] if len(df[col].mode()) > 0 else 'Unknown'
                df_imputed[col].fillna(mode_val, inplace=True)
    
    return df_imputed


