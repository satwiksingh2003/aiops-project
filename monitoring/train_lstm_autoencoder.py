# =====================================================
# AIOps LSTM Autoencoder Training
# =====================================================
import joblib
import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    Input,
    LSTM,
    RepeatVector,
    TimeDistributed,
    Dense
)

# =====================================================
# Configuration
# =====================================================

DATASET_PATH = "monitoring/clean_dataset.csv"

FEATURES = [
    "CPU",
    "Memory_MB",
    "Network_RX_KBps",
    "Network_TX_KBps"
]

# =====================================================
# Load Dataset
# =====================================================

print("=" * 60)
print("Loading Dataset")
print("=" * 60)

df = pd.read_csv(DATASET_PATH)

print(f"Dataset Shape : {df.shape}")

# =====================================================
# Select Features
# =====================================================

data = df[FEATURES]

print("\nSelected Features:")
print(data.head())

# =====================================================
# Normalize Data
# =====================================================

print("\nNormalizing Data...")

scaler = MinMaxScaler()

scaled_data = scaler.fit_transform(data)

print("Normalization Completed.")

print(f"Scaled Data Shape : {scaled_data.shape}")

# =====================================================
# Create Time Sequences
# =====================================================

SEQUENCE_LENGTH = 5


def create_sequences(data, sequence_length):
    """
    Convert the normalized data into
    sequences for LSTM training.
    """

    sequences = []

    for i in range(len(data) - sequence_length):

        sequence = data[i:i + sequence_length]

        sequences.append(sequence)

    return sequences


print("\nCreating sequences...")

X_train = create_sequences(
    scaled_data,
    SEQUENCE_LENGTH
)

import numpy as np

X_train = np.array(X_train)

print("Sequence creation completed.")

print(f"Training Data Shape : {X_train.shape}")

# =====================================================
# Build LSTM Autoencoder
# =====================================================

print("\nBuilding LSTM Autoencoder...")

timesteps = X_train.shape[1]
features = X_train.shape[2]

# Encoder
inputs = Input(shape=(timesteps, features))

encoded = LSTM(
    32,
    activation="relu",
    return_sequences=True
)(inputs)

encoded = LSTM(
    16,
    activation="relu",
    return_sequences=False
)(encoded)

# Decoder
decoded = RepeatVector(timesteps)(encoded)

decoded = LSTM(
    16,
    activation="relu",
    return_sequences=True
)(decoded)

decoded = LSTM(
    32,
    activation="relu",
    return_sequences=True
)(decoded)

outputs = TimeDistributed(
    Dense(features)
)(decoded)

model = Model(inputs, outputs)

model.compile(
    optimizer="adam",
    loss="mse"
)

print("Model created successfully.\n")

model.summary()

# =====================================================
# Train LSTM Autoencoder
# =====================================================

print("\n")
print("=" * 60)
print("Training LSTM Autoencoder")
print("=" * 60)

history = model.fit(
    X_train,
    X_train,
    epochs=30,
    batch_size=16,
    validation_split=0.2,
    shuffle=False,
    verbose=1
)

print("\nTraining completed successfully.")

# =====================================================
# Save Model
# =====================================================

os.makedirs("models", exist_ok=True)

model.save("models/lstm_autoencoder.keras")

joblib.dump(
    scaler,
    "models/scaler.pkl"
)

print("\n")
print("=" * 60)
print("Model Saved")
print("=" * 60)

print("LSTM Model : models/lstm_autoencoder.keras")
print("Scaler     : models/scaler.pkl")

# =====================================================
# Reconstruction
# =====================================================

print("\n")
print("=" * 60)
print("Reconstructing Training Data")
print("=" * 60)

reconstructed = model.predict(X_train)

print("Reconstruction completed.")

# =====================================================
# Reconstruction Error
# =====================================================

errors = np.mean(
    np.square(X_train - reconstructed),
    axis=(1, 2)
)

print(f"\nTotal Sequences : {len(errors)}")

print(f"Minimum Error : {errors.min():.6f}")
print(f"Maximum Error : {errors.max():.6f}")
print(f"Average Error : {errors.mean():.6f}")

# =====================================================
# Threshold
# =====================================================

threshold = np.percentile(errors, 95)

print(f"\nAnomaly Threshold : {threshold:.6f}")

predictions = errors > threshold

print(f"Detected Anomalies : {predictions.sum()}")
print(f"Normal Sequences   : {len(predictions) - predictions.sum()}")