# Data source

## Origin

IBM Telco Customer Churn — commit-pinned snapshot:
<https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/1fd6fd70906479be1712e64cfc0ea89f58466629/data/Telco-Customer-Churn.csv>

The supplied copy (telco.csv) was provided by the instructor and is presumed to be the same bytes as the pinned URL above. This has not been independently verified against a fresh download.

## Local location
- Path inside the project: data/raw/telco.csv
- Size: 970,457 bytes
- Kept outside Git (see .gitignore). The original snapshot is immutable; no cleanup is done in TP01.

## Verification

SHA-256 of the local file:

16320c9c1ec72448db59aa0a26a0b95401046bef5d02fd3aeb906448e3055e91

To verify a fresh copy on Windows PowerShell:

(Get-FileHash data\raw\telco.csv -Algorithm SHA256).Hash.ToLower()

It must return the value above. A matching hash confirms byte identity with the file used in this project — it does not prove the business data is correct, only that the file has not changed.

## Fields (roles for TP02)

| Role | Column(s) |
|---|---|
| Identifier | customerID |
| Target | Churn (Yes / No) |
| Potential numeric inputs | tenure, MonthlyCharges, TotalCharges |
| Potential categorical inputs | Contract, InternetService, PaymentMethod, and others |

## Known quirks


- TotalCharges is read as text (str), not numeric. 11 rows contain an empty/whitespace-only value. isna() does not flag them. This is why naive 'no missing values' checks are wrong for this dataset.
- This is a customer snapshot, not a dated event history and not a randomized retention experiment. Do not interpret any association as causal.
