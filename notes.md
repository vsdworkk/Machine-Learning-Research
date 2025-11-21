## Service Provider Reputation Score

The Service Provider Reputation Score is a behavioral feature designed to quantify the historical reliability of the firm submitting the claim, operating on the premise that past accuracy is a strong predictor of future performance. To prevent data leakage during model training, this score is calculated using Leave-One-Out Target Encoding: for every specific claim, the model calculates the average reliability of all other claims submitted by that provider, strictly excluding the current claim from the calculation. This technique ensures the model judges the provider based solely on their historical track record without "cheating" by seeing the outcome of the case currently being predicted, while new or unknown providers are assigned the global average reliability to maintain a neutral baseline.

## Industry Wage Ratio

The Industry Wage Ratio identifies potential anomalies by comparing the specific wage claimed by the Insolvency Practitioner against the standard wage for that industry, using external benchmark data from Jobs and Skills Australia (JSA). We calculated this feature by dividing the IP Weekly Wage by the JSA median wage for the corresponding industry.

## Employee Tenure 

The Employee Tenure feature converts raw calendar dates into a numeric duration representing years of service, which is the primary determinant for Long Service Leave (LSL) eligibility. We calculated this by finding the difference between the IP Termination Date and IP Commencement Date and dividing by 365.25. To ensure data integrity, we corrected physically impossible negative tenures to zero and imputed missing records with a sentinel value of -9999. This imputation strategy prevents the model from assuming an "average" tenure for missing data, instead forcing it to treat unknown employment periods as a distinct risk category—a technique specifically optimized for tree-based algorithms like XGBoost and LightGBM.

## Count of Instruments for Case Industry (This is available in the GI Dataset).

## Potential Models to Consider

XGBoost Classifier is the industry standard for this dataset because it natively handles our -9999 tenure sentinels and automatically corrects class imbalance via the scale_pos_weight parameter. It excels at detecting rare risk cases in high-stakes data and provides the robust feature importance metrics required for stakeholder explainability, making it the strongest candidate for accuracy.

LightGBM offers a high-speed alternative using "leaf-wise" growth, which is exceptionally effective at isolating complex, specific risk pockets like high-wage claims in niche industries. It is significantly faster than XGBoost, making it ideal for rapid experimentation and frequent retraining, though it requires strict regularization to prevent overfitting on datasets with fewer than 50,000 rows.

Logistic Regression acts as a mandatory baseline to verify if complex algorithms are necessary, offering a purely linear "white box" interpretation where every dollar increase in wages has a fixed, calculable impact on risk. While likely to have lower recall than boosting models, it provides the highest level of transparency for auditors and serves as a crucial sanity check for the more complex engines.

To optimize these models, we employ Stratified K-Fold Cross-Validation combined with Randomized Search, splitting the data into five distinct chunks that preserve the exact 95/5 risk ratio found in the real world. This process automatically tests dozens of configuration combinations—such as tree depth and learning rate—and scores them strictly on Recall, ensuring the final model is mathematically tuned to prioritize catching errors over simple accuracy.

