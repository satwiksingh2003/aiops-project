# =====================================================
# Hybrid Anomaly Detection Engine
# =====================================================

import joblib
import numpy as np
import pandas as pd
import tensorflow as tf

from config import FEATURES

# -----------------------------------------------------
# Load Models
# -----------------------------------------------------

print("=" * 60)
print("Loading Hybrid Detection Models")
print("=" * 60)

isolation_forest = joblib.load(
    "monitoring/isolation_forest_model.pkl"
)

lstm_model = tf.keras.models.load_model(
    "models/lstm_autoencoder.keras"
)

scaler = joblib.load(
    "models/scaler.pkl"
)

print("Isolation Forest Loaded")
print("LSTM Autoencoder Loaded")
print("Scaler Loaded")

# =====================================================
# Hybrid Prediction
# =====================================================

SEQUENCE_LENGTH = 5
LSTM_THRESHOLD = 0.017606


def hybrid_predict(sequence):
    """
    Parameters
    ----------
    sequence : numpy.ndarray
        Shape = (5, 4)

    Returns
    -------
    dict
        Isolation Forest prediction,
        LSTM prediction,
        Reconstruction error,
        Final hybrid decision.
    """

    # -----------------------------
    # Isolation Forest Prediction
    # -----------------------------

    latest_sample_df = pd.DataFrame(
        [sequence[-1]],
        columns=FEATURES
    )

    isolation_prediction = isolation_forest.predict(
        latest_sample_df
    )[0]

    # -----------------------------
    # LSTM Prediction
    # -----------------------------

    sequence_df = pd.DataFrame(
        sequence,
        columns=FEATURES
    )

    scaled_sequence = scaler.transform(
        sequence_df
    )

    scaled_sequence = scaled_sequence.reshape(
        1,
        SEQUENCE_LENGTH,
        len(FEATURES)
    )

    reconstructed = lstm_model.predict(
        scaled_sequence,
        verbose=0
    )

    error = np.mean(
        np.square(
            scaled_sequence - reconstructed
        )
    )

    lstm_prediction = (
        -1 if error > LSTM_THRESHOLD else 1
    )

    # -----------------------------
    # Hybrid Decision
    # -----------------------------

    if isolation_prediction == -1 and lstm_prediction == -1:

        decision = "HIGH_CONFIDENCE_ANOMALY"

    elif isolation_prediction == -1 or lstm_prediction == -1:

        decision = "SUSPICIOUS"

    else:

        decision = "NORMAL"

    return {
        "IsolationForest": isolation_prediction,
        "LSTM": lstm_prediction,
        "ReconstructionError": float(error),
        "Decision": decision
    }


# =====================================================
# Test Hybrid Detection
# =====================================================

if __name__ == "__main__":

    sample = np.array([
        [0.001, 30.0, 0.01, 0.01],
        [0.002, 32.0, 0.02, 0.02],
        [0.003, 31.0, 0.02, 0.02],
        [0.002, 30.0, 0.03, 0.02],
        [0.001, 31.0, 0.02, 0.03]
    ])

    result = hybrid_predict(sample)

    print("\n" + "=" * 60)
    print("Hybrid Prediction Result")
    print("=" * 60)

    for key, value in result.items():
        print(f"{key:22}: {value}")