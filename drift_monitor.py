import pandas as pd

# Load dataset
df = pd.read_csv("online_retail_II.csv", encoding="ISO-8859-1")

# Convert date column
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Remove rows with missing values in important columns
df = df.dropna(subset=["Quantity", "Price", "InvoiceDate"])

# Keep only valid transactions
df = df[(df["Quantity"] > 0) & (df["Price"] > 0)]

print("Cleaned dataset shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())

# Create additional features
df["Sales"] = df["Quantity"] * df["Price"]

df["Month"] = df["InvoiceDate"].dt.month

df["DayOfWeek"] = df["InvoiceDate"].dt.dayofweek

df["Demand"] = df["Quantity"]

print("\nFeatures created:")
print(df[[
    "Price",
    "Demand",
    "Sales",
    "Month",
    "DayOfWeek"
]].head())

# Sort by date
df = df.sort_values("InvoiceDate")

# Split data into historical and recent data
split_index = int(len(df) * 0.7)

reference_data = df.iloc[:split_index].copy()
current_data = df.iloc[split_index:].copy()

# Features to monitor
features = [
    "Price",
    "Demand",
    "Sales",
    "Month",
    "DayOfWeek"
]

reference_data = reference_data[features]
current_data = current_data[features]

print("\nReference data:", reference_data.shape)
print("Current data:", current_data.shape)

# Simulate changes in production data
current_data["Price"] = current_data["Price"] * 1.25

current_data["Demand"] = current_data["Demand"] * 0.75

print("\nProduction drift simulated.")

from evidently import Report
from evidently.presets import DataDriftPreset

# Create drift report
report = Report([
    DataDriftPreset()
])

# Compare reference and current data
result = report.run(
    reference_data=reference_data,
    current_data=current_data
)

print("\nEvidently drift analysis completed.")

# Save the report
result.save_html("reports/retail_drift_report.html")

print("Drift report generated successfully!")

result = report.run(
    reference_data=reference_data,
    current_data=current_data
)