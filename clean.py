import pandas as pd
import numpy as np

def master_data_pipeline(df_raw, df_abs):
    """
    End-to-End Pipeline:
    1. Sanitizes Targets (0-1 range)
    2. Engineers Internal Features (Tenure)
    3. Enriches with External ABS Data (Wage Ratios)
    4. Drops Leakage & Raw Data
    5. Handles Outliers & Missing Values
    """
    df = df_raw.copy()
    print(f"Original Shape: {df.shape}")

    # ==============================================================================
    # 1. TARGET SANITIZATION
    # ==============================================================================
    target_cols = [
        'Annual Leave Reliability', 
        'Long Service Leave Reliability', 
        'Wages Reliability'
    ]
    
    for col in target_cols:
        if col in df.columns:
            # Clip negatives to 0 (Massive Error = 0% Reliable)
            df[col] = df[col].clip(lower=0.0, upper=1.0)
            # Drop rows where the Target is NaN (cannot train on them)
            df = df.dropna(subset=[col])

    # ==============================================================================
    # 2. INTERNAL FEATURE ENGINEERING
    # ==============================================================================
    
    # A. TENURE (Time is Money)
    df['IP Commencement Date'] = pd.to_datetime(df['IP Commencement Date'], errors='coerce')
    df['IP Termination Date'] = pd.to_datetime(df['IP Termination Date'], errors='coerce')
    
    # Calculate Tenure in Years
    df['IP_Tenure_Years'] = (df['IP Termination Date'] - df['IP Commencement Date']).dt.days / 365.25
    
    # Fix impossible negative tenure and fill missing with -1
    df.loc[df['IP_Tenure_Years'] < 0, 'IP_Tenure_Years'] = 0
    df['IP_Tenure_Years'] = df['IP_Tenure_Years'].fillna(-1)

    # ==============================================================================
    # 3. EXTERNAL ABS INTEGRATION (Your ABS Logic)
    # ==============================================================================
    if 'Industry' in df.columns:
        # Validate Match
        unique_main_ind = set(df['Industry'].dropna().unique())
        unique_abs_ind = set(df_abs['Industry'].unique())
        missing_industries = unique_main_ind - unique_abs_ind
        if missing_industries:
            print(f"WARNING: Missing ABS matches for: {missing_industries}")

        # Merge
        df = df.merge(df_abs[['Industry', 'ABS_Average_Weekly_Wage']], on='Industry', how='left')
        
        # Fill missing ABS wages with National Median
        national_median = df_abs['ABS_Average_Weekly_Wage'].median()
        df['ABS_Average_Weekly_Wage'] = df['ABS_Average_Weekly_Wage'].fillna(national_median)
        
        # Create Ratio Feature
        df['IP_Wage_to_ABS_Ratio'] = df['IP Weekly Wage'] / (df['ABS_Average_Weekly_Wage'] + 1e-5)
        df['Flag_High_Wage_Deviation'] = (df['IP_Wage_to_ABS_Ratio'] > 1.5).astype(int)
        
        # Drop the raw dollar value (optional, but recommended to reduce noise)
        df.drop(columns=['ABS_Average_Weekly_Wage'], inplace=True)

    # ==============================================================================
    # 4. PREVENT LEAKAGE (Dropping Columns)
    # ==============================================================================
    
    cols_to_drop = [
        # Group 1: Claimant Data (Unavailable at inference)
        'Claim ID', 'Claim Type', 'Claim Form Received Date', 'Claimant Age', 
        'Service Years At Appointment', 'Job Title', 'Job Duty Description', 
        'Claimant Confident of Amounts Owed', 'Information Held About Owed Entitlements',
        'Claimant Commencement Date', 'Claimant Termination Date', 
        'Claimant Weekly Wage', 'Claimant Annual Leave', 'Claimant Wages',
        
        # Group 2: CM Recommended Data (THE ANSWER KEY - MUST DROP)
        'CM Recommended Employment Type', 'CM Recommended Weekly Wage', 
        'CM Recommended Commencement Date', 'CM Recommended Termination Date',
        'CM Recommended Annual Leave', 'CM Recommended Long Service Leave', 
        'CM Recommended Wages',
        
        # Raw Dates (We now have Tenure)
        'IP Commencement Date', 'IP Termination Date'
    ]
    
    # Only drop columns that actually exist
    existing_cols_to_drop = [c for c in cols_to_drop if c in df.columns]
    df.drop(columns=existing_cols_to_drop, inplace=True)

    # ==============================================================================
    # 5. OUTLIER TREATMENT (Winsorization)
    # ==============================================================================
    
    days_col = 'Days Between IP Verified Data Request and Received Date'
    if days_col in df.columns:
        df = df[df[days_col] >= 0] # Remove impossible negatives
        upper_limit = df[days_col].quantile(0.99) # Cap extreme delays
        df.loc[df[days_col] > upper_limit, days_col] = upper_limit

    # ==============================================================================
    # 6. FINAL IMPUTATION
    # ==============================================================================
    
    for col in df.columns:
        if df[col].isna().sum() > 0:
            # Add 'is_missing' flag for better model context
            df[f'{col}_missing'] = df[col].isna().astype(int)
            
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].median())
            else:
                mode_val = df[col].mode()[0] if not df[col].mode().empty else 'Unknown'
                df[col] = df[col].fillna(mode_val)

    print(f"Final Shape: {df.shape}")
    return df

    # 1. Load your raw datasets (Change filenames to match your actual files)
df_main_raw = pd.read_csv('FEG_Main_Dataset.csv') 
df_abs_raw = pd.read_csv('ABS_Industry_Wages.csv') 

# 2. Run the Master Pipeline
# This cleans df_main_raw using the rules we wrote and the ABS data
df_final = master_data_pipeline(df_main_raw, df_abs_raw)

# 3. Verification Checks
print("\n--- Reliability Scores (Should be between 0.0 and 1.0) ---")
print(df_final[['Wages Reliability', 'Annual Leave Reliability']].describe())

print("\n--- Check for Leakage (Should be empty) ---")
leakage_cols = [c for c in df_final.columns if 'CM Recommended' in c]
print(f"Leaking columns remaining: {leakage_cols}")

print("\n--- Check New Features ---")
print(df_final[['IP_Tenure_Years', 'IP_Wage_to_ABS_Ratio']].head())