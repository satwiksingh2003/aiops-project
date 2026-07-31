# =====================================================
# AIOps - Isolation Forest Training
# =====================================================

import pandas as pd

from sklearn.ensemble import IsolationForest

import joblib

# =====================================================
# Load Dataset
# =====================================================

print("Loading dataset...")

df = pd.read_csv("monitoring/clean_dataset.csv")

print("\nDataset Loaded Successfully!")

print(df.head())

# =====================================================
# Feature Selection
# =====================================================

print("\nSelecting Features for Training...")

features = [
    "CPU",
    "Memory_MB",
    "Network_RX_KBps",
    "Network_TX_KBps"
]

X = df[features]

print("\nSelected Features:")

print(X.head())

# =====================================================
# Train Isolation Forest
# =====================================================

print("\nTraining Isolation Forest Model...")

model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42
)

model.fit(X)

print("\nModel Trained Successfully!")

# =====================================================
# Predict Anomalies
# =====================================================

print("\nDetecting Anomalies...")

predictions = model.predict(X)

df["Prediction"] = predictions

print("\nPrediction Results:")

print(df[["CPU", "Memory_MB", "Prediction"]].head(10))

# =====================================================
# Count Normal and Anomalies
# =====================================================

normal_count = (predictions == 1).sum()

anomaly_count = (predictions == -1).sum()

print("\nSummary")

print("Normal Samples :", normal_count)

print("Anomalies      :", anomaly_count)

# =====================================================
# Save Trained Model
# =====================================================

print("\nSaving Model...")

joblib.dump(model, "monitoring/isolation_forest_model.pkl")

print("Model saved successfully!")

# =====================================================
# Save Prediction Results
# =====================================================

df.to_csv("monitoring/prediction_results.csv", index=False)

print("Prediction results saved successfully!")

# =====================================================
# Display Detected Anomalies
# =====================================================

print("\nDetected Anomalies:")

anomalies = df[df["Prediction"] == -1]

print(anomalies)