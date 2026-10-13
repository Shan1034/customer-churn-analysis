
import pandas as pd

# 1. Load the original dataset
df = pd.read_csv("data/Telco-Customer-Churn.csv")

print("ORIGINAL DATASET")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# 2. Convert TotalCharges from text to numeric
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"].astype(str).str.strip(),
    errors="coerce"
)

# 3. Check the new data type
print("\nTOTALCHARGES DATA TYPE")
print(df["TotalCharges"].dtype)

# 4. Count missing TotalCharges values
print("\nMISSING TOTALCHARGES VALUES")
print(df["TotalCharges"].isna().sum())

# 5. Display customers with missing TotalCharges
missing_charges = df[df["TotalCharges"].isna()]

print("\nCUSTOMERS WITH MISSING TOTALCHARGES")
print(
    missing_charges[
        ["customerID", "tenure", "MonthlyCharges", "TotalCharges", "Churn"]
    ].to_string(index=False)
)

# 6. Check the tenure of these customers
print("\nTENURE OF CUSTOMERS WITH MISSING TOTALCHARGES")
print(missing_charges["tenure"].value_counts().sort_index())

# 7. Confirm that no customer records were deleted
print("\nFINAL DATASET DIMENSIONS")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


# STEP 5: CUSTOMER CHURN ANALYSIS

# 1. Count customers who left
churned_customers = (df["Churn"] == "Yes").sum()

# 2. Count customers who stayed
retained_customers = (df["Churn"] == "No").sum()

# 3. Count all customers
total_customers = len(df)

# 4. Calculate the overall churn rate
churn_rate = (churned_customers / total_customers) * 100

# 5. Display the results
print("\nCUSTOMER CHURN ANALYSIS")
print("Total customers:", total_customers)
print("Customers who churned:", churned_customers)
print("Customers who stayed:", retained_customers)
print("Overall churn rate:", round(churn_rate, 2), "%")


# STEP 6: CHURN ANALYSIS BY CONTRACT TYPE

# 1. Group customers by contract type and churn status
contract_churn = df.groupby(["Contract", "Churn"]).size().unstack(fill_value=0)

# 2. Calculate total customers in each contract type
contract_churn["Total Customers"] = (
    contract_churn["Yes"] + contract_churn["No"]
)

# 3. Calculate churn rate for each contract type
contract_churn["Churn Rate (%)"] = (
    contract_churn["Yes"] / contract_churn["Total Customers"] * 100
)

# 4. Display the results
print("\nCHURN ANALYSIS BY CONTRACT TYPE")
print(contract_churn.round(2))


# STEP 7: CHURN ANALYSIS BY CUSTOMER TENURE

# 1. Create groups based on months as a customer
tenure_bins = [0, 12, 24, 48, 72]

tenure_labels = [
    "0-12 months",
    "13-24 months",
    "25-48 months",
    "49-72 months"
]

df["TenureGroup"] = pd.cut(
    df["tenure"],
    bins=tenure_bins,
    labels=tenure_labels,
    include_lowest=True
)

# 2. Count churned and retained customers in each group
tenure_churn = (
    df.groupby(["TenureGroup", "Churn"], observed=False)
    .size()
    .unstack(fill_value=0)
)

# 3. Calculate total customers in each group
tenure_churn["Total Customers"] = (
    tenure_churn["Yes"] + tenure_churn["No"]
)

# 4. Calculate churn rate for each group
tenure_churn["Churn Rate (%)"] = (
    tenure_churn["Yes"] / tenure_churn["Total Customers"] * 100
)

# 5. Display the results
print("\nCHURN ANALYSIS BY TENURE GROUP")
print(tenure_churn.round(2))


# STEP 8: CHURN ANALYSIS BY MONTHLY CHARGES

# 1. Define monthly charge ranges
charge_bins = [0, 35, 65, 90, 120]

charge_labels = [
    "0-35",
    "35-65",
    "65-90",
    "90-120"
]

# 2. Assign each customer to a charge group
df["MonthlyChargeGroup"] = pd.cut(
    df["MonthlyCharges"],
    bins=charge_bins,
    labels=charge_labels,
    include_lowest=True
)

# 3. Count churned and retained customers in each group
charge_churn = (
    df.groupby(
        ["MonthlyChargeGroup", "Churn"],
        observed=False
    )
    .size()
    .unstack(fill_value=0)
)

# 4. Calculate total customers per group
charge_churn["Total Customers"] = (
    charge_churn["Yes"] + charge_churn["No"]
)

# 5. Calculate churn rate
charge_churn["Churn Rate (%)"] = (
    charge_churn["Yes"]
    / charge_churn["Total Customers"]
    * 100
)

# 6. Display results
print("\nCHURN ANALYSIS BY MONTHLY CHARGES")
print(charge_churn.round(2))


# STEP 9: CHURN ANALYSIS BY PAYMENT METHOD

# 1. Count customers by payment method and churn status
payment_churn = (
    df.groupby(["PaymentMethod", "Churn"])
    .size()
    .unstack(fill_value=0)
)

# 2. Calculate the total customers for each payment method
payment_churn["Total Customers"] = (
    payment_churn["Yes"] + payment_churn["No"]
)

# 3. Calculate the churn rate for each payment method
payment_churn["Churn Rate (%)"] = (
    payment_churn["Yes"]
    / payment_churn["Total Customers"]
    * 100
)

# 4. Display the results, highest churn rate first
payment_churn = payment_churn.sort_values(
    by="Churn Rate (%)",
    ascending=False
)

print("\nCHURN ANALYSIS BY PAYMENT METHOD")
print(payment_churn.round(2))


# STEP 10: COMBINED CHURN SUMMARY

# 1. Create a list to store our findings
summary_data = []

# 2. Summarise churn by contract type
for group, data in df.groupby("Contract"):
    total = len(data)
    churned = (data["Churn"] == "Yes").sum()
    rate = churned / total * 100

    summary_data.append({
        "Factor": "Contract",
        "Group": group,
        "Total Customers": total,
        "Churned Customers": churned,
        "Churn Rate (%)": round(rate, 2)
    })

# 3. Summarise churn by tenure group
for group, data in df.groupby("TenureGroup", observed=True):
    total = len(data)
    churned = (data["Churn"] == "Yes").sum()
    rate = churned / total * 100

    summary_data.append({
        "Factor": "Tenure",
        "Group": str(group),
        "Total Customers": total,
        "Churned Customers": churned,
        "Churn Rate (%)": round(rate, 2)
    })

# 4. Summarise churn by monthly-charge group
for group, data in df.groupby("MonthlyChargeGroup", observed=True):
    total = len(data)
    churned = (data["Churn"] == "Yes").sum()
    rate = churned / total * 100

    summary_data.append({
        "Factor": "Monthly Charges",
        "Group": str(group),
        "Total Customers": total,
        "Churned Customers": churned,
        "Churn Rate (%)": round(rate, 2)
    })

# 5. Summarise churn by payment method
for group, data in df.groupby("PaymentMethod"):
    total = len(data)
    churned = (data["Churn"] == "Yes").sum()
    rate = churned / total * 100

    summary_data.append({
        "Factor": "Payment Method",
        "Group": group,
        "Total Customers": total,
        "Churned Customers": churned,
        "Churn Rate (%)": round(rate, 2)
    })

# 6. Convert our list into a table
summary_df = pd.DataFrame(summary_data)

# 7. Sort the results by churn rate
summary_df = summary_df.sort_values(
    by="Churn Rate (%)",
    ascending=False
)

# 8. Display the combined summary
print("\nCOMBINED CHURN SUMMARY")
print(summary_df.to_string(index=False))


# STEP 11: EXPORT THE COMBINED SUMMARY

summary_df.to_csv(
    "churn_summary.csv",
    index=False
)

print("\nCombined churn summary saved as churn_summary.csv")


# STEP 12: EXPORT THE FULL DATASET FOR POWER BI

df.to_csv(
    "customer_churn_cleaned.csv",
    index=False
)

print("\nFull customer dataset saved for Power BI.")
print("Rows exported:", len(df))
print("Columns exported:", len(df.columns))




