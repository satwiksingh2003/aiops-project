import pandas as pd

# ---------------- Load Dataset ----------------
df = pd.read_csv("monitoring/dataset.csv")

print("=" * 60)
print("AIOps Dataset Analysis")
print("=" * 60)

# ---------------- Basic Information ----------------
print("\nDataset Information:\n")
df.info()

# ---------------- Shape ----------------
print("\nDataset Shape:")
print(df.shape)

# ---------------- First Five Rows ----------------
print("\nFirst 5 Rows:\n")
print(df.head())

# ---------------- Last Five Rows ----------------
print("\nLast 5 Rows:\n")
print(df.tail())

# ---------------- Missing Values ----------------
print("\nMissing Values:\n")
print(df.isnull().sum())

# ---------------- Duplicate Rows ----------------
print("\nDuplicate Rows:")
print(df.duplicated().sum())

# ---------------- Data Types ----------------
print("\nData Types:\n")
print(df.dtypes)

# ---------------- Statistical Summary ----------------
print("\nStatistical Summary:\n")
print(df.describe())

# ---------------- Remove Duplicates ----------------
df.drop_duplicates(inplace=True)

# ---------------- Save Clean Dataset ----------------
df.to_csv(
    "monitoring/clean_dataset.csv",
    index=False
)

print("\nClean dataset saved successfully!")