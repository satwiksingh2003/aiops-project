# =====================================================
# AIOps Real-Time Anomaly Detection
# =====================================================

import joblib
import pandas as pd
import time

from metrics_collector import collect_metrics
from remediation import recommend_action, restart_pod
from logger import logger

# =====================================================
# Configuration
# =====================================================

MODEL_PATH = "monitoring/isolation_forest_model.pkl"

FEATURES = [
    "CPU",
    "Memory_MB",
    "Network_RX_KBps",
    "Network_TX_KBps"
]

# =====================================================
# Load Model
# =====================================================

print("=" * 60)
print("Loading Isolation Forest Model")
print("=" * 60)

try:

    model = joblib.load(MODEL_PATH)

    print("Model loaded successfully.\n")
    logger.info("Isolation Forest model loaded successfully.")

except Exception as e:

    print("Unable to load model.")
    print(e)
    logger.error(f"Unable to load model: {e}")
    exit()


# =====================================================
# Detection Function
# =====================================================

def detect_and_remediate():
    """
    Collect live metrics, detect anomalies,
    recommend remediation actions,
    and perform self-healing.
    """

    # =====================================================
    # Collect Metrics
    # =====================================================

    print("Collecting live metrics...\n")
    logger.info("Collecting live metrics from Kubernetes cluster.")

    try:

        live_metrics = collect_metrics()

    except Exception as e:

        print("Metric collection failed.")
        print(e)

        logger.error(f"Metric collection failed: {e}")

        return

    # =====================================================
    # Prediction
    # =====================================================

    prediction_data = live_metrics[FEATURES]

    prediction = model.predict(prediction_data)

    live_metrics["Prediction"] = prediction

    live_metrics["Status"] = live_metrics["Prediction"].map({
        1: "NORMAL",
        -1: "ANOMALY"
    })

    # =====================================================
    # Display Pod Status
    # =====================================================

    print("\n")
    print("=" * 60)
    print("Pod Status Summary")
    print("=" * 60)

    print(
        live_metrics[
            [
                "Pod",
                "CPU",
                "Memory_MB",
                "Network_RX_KBps",
                "Network_TX_KBps",
                "Status"
            ]
        ]
    )

    # =====================================================
    # Detection Summary
    # =====================================================

    total = len(live_metrics)
    normal = (live_metrics["Prediction"] == 1).sum()
    anomaly = (live_metrics["Prediction"] == -1).sum()

    print("\n")
    print("=" * 60)
    print("AIOps Detection Summary")
    print("=" * 60)

    print(f"Total Pods      : {total}")
    print(f"Normal Pods     : {normal}")
    print(f"Anomalous Pods  : {anomaly}")

    logger.info(
        f"Pods Scanned={total} | Normal={normal} | Anomalies={anomaly}"
    )

    # =====================================================
    # Recommendation Engine
    # =====================================================

    if anomaly > 0:

        anomalies = live_metrics[
            live_metrics["Prediction"] == -1
        ].copy()

        logger.warning(f"{len(anomalies)} anomalous pod(s) detected.")

        actions = anomalies.apply(
            recommend_action,
            axis=1,
            result_type="expand"
        )

        anomalies["Recommended_Action"] = actions[0]
        anomalies["Reason"] = actions[1]

        print("\n")
        print("=" * 60)
        print("Recommended Actions")
        print("=" * 60)

        print(
            anomalies[
                [
                    "Pod",
                    "CPU",
                    "Memory_MB",
                    "Network_RX_KBps",
                    "Network_TX_KBps",
                    "Recommended_Action",
                    "Reason"
                ]
            ]
        )

        anomalies.to_csv(
            "monitoring/anomaly_report.csv",
            index=False
        )

        logger.info("Anomaly report saved.")

        print("\nAnomaly report saved to monitoring/anomaly_report.csv")

        # =====================================================
        # Self-Healing Engine
        # =====================================================

        print("\n")
        print("=" * 60)
        print("Self-Healing Engine")
        print("=" * 60)

        for _, row in anomalies.iterrows():

            pod = row["Pod"]
            action = row["Recommended_Action"]

            logger.info(
                f"Pod={pod} | Recommended Action={action}"
            )

            if action == "Restart Pod":

                logger.warning(f"Restarting pod {pod}")

                restart_pod(pod)

            else:

                logger.warning(
                    f"No automatic remediation configured for {pod}"
                )

                print(f"\nNo automatic remediation configured for {pod}")
                print(f"Recommended Action : {action}")
                print(f"Reason             : {row['Reason']}")

    else:

        print("\nNo anomalies detected.")
        logger.info("No anomalies detected.")


# =====================================================
# Main Function
# =====================================================

def main():
    """
    Entry point of the AIOps engine.
    Runs continuously.
    """

    logger.info("AIOps Monitoring Service Started.")

    while True:

        detect_and_remediate()

        logger.info("Sleeping for 10 seconds before next health check.")

        print("\nWaiting 10 seconds before next health check...\n")

        time.sleep(10)


# =====================================================
# Program Entry Point
# =====================================================

if __name__ == "__main__":
    main()