# =====================================================
# Hybrid AIOps Real-Time Monitoring Engine
# =====================================================

import time
import os
from datetime import datetime
from collections import defaultdict, deque

import pandas as pd

from metrics_collector import collect_metrics
from remediation import recommend_action, restart_pod
from logger import logger
from hybrid_detection import hybrid_predict

from config import FEATURES, CHECK_INTERVAL
from prometheus_client import Gauge, start_http_server

# =====================================================
# Rolling Window Configuration
# =====================================================

WINDOW_SIZE = 5

# Stores the latest metric history of every pod
pod_history = defaultdict(
    lambda: deque(maxlen=WINDOW_SIZE)
)

print("=" * 60)
print("Hybrid AIOps Monitoring Engine Started")
print("=" * 60)

logger.info("Hybrid AIOps Monitoring Engine Started")

# =====================================================
# Prometheus Metrics
# =====================================================

TOTAL_PODS = Gauge(
    "aiops_total_pods",
    "Total pods monitored"
)

NORMAL_PODS = Gauge(
    "aiops_normal_pods",
    "Pods classified as NORMAL"
)

SUSPICIOUS_PODS = Gauge(
    "aiops_suspicious_pods",
    "Pods classified as SUSPICIOUS"
)

HIGH_CONFIDENCE_ANOMALIES = Gauge(
    "aiops_high_confidence_anomalies",
    "Pods classified as HIGH_CONFIDENCE_ANOMALY"
)
# =====================================================
# Detection Function
# =====================================================

def detect_and_remediate():

    print("\nCollecting live metrics...\n")

    logger.info(
        "Collecting live metrics from Kubernetes cluster."
    )

    try:

        live_metrics = collect_metrics()

    except Exception as e:

        print("Metric collection failed.")

        print(e)

        logger.error(e)

        return

    # -----------------------------------------
    # Hybrid Detection
    # -----------------------------------------

    predictions = []

    decisions = []

    reconstruction_errors = []

    for _, row in live_metrics.iterrows():

        pod = row["Pod"]
        
        sample = row[FEATURES].astype(float).to_numpy()

        pod_history[pod].append(sample)
        
        if len(pod_history[pod]) < WINDOW_SIZE:

            predictions.append(1)

            decisions.append("COLLECTING_HISTORY")

            reconstruction_errors.append(0.0)

            continue

        sequence = list(pod_history[pod])

        result = hybrid_predict(sequence)

        reconstruction_errors.append(
            result["ReconstructionError"]
        )

        decisions.append(
            result["Decision"]
        )

        if result["Decision"] == "NORMAL":

            predictions.append(1)

        else:

            predictions.append(-1)

    live_metrics["Prediction"] = predictions

    live_metrics["Decision"] = decisions

    live_metrics["ReconstructionError"] = reconstruction_errors

    # =====================================================
    # Pod Status Summary
    # =====================================================

    print("\n")
    print("=" * 60)
    print("Hybrid Pod Status Summary")
    print("=" * 60)

    print(
        live_metrics[
            [
                "Pod",
                "CPU",
                "Memory_MB",
                "Network_RX_KBps",
                "Network_TX_KBps",
                "Decision",
                "ReconstructionError"
            ]
        ]
    )

    # =====================================================
    # Detection Summary
    # =====================================================

    total = len(live_metrics)

    collecting = (
        live_metrics["Decision"] == "COLLECTING_HISTORY"
    ).sum()

    normal = (
        live_metrics["Decision"] == "NORMAL"
    ).sum()

    suspicious = (
        live_metrics["Decision"] == "SUSPICIOUS"
    ).sum()

    anomalies = (
        live_metrics["Decision"] == "HIGH_CONFIDENCE_ANOMALY"
    ).sum()

    print("\n")
    print("=" * 60)
    print("Hybrid Detection Summary")
    print("=" * 60)

    print(f"Total Pods                 : {total}")
    print(f"Collecting History         : {collecting}")
    print(f"Normal Pods                : {normal}")
    print(f"Suspicious Pods            : {suspicious}")
    print(f"High Confidence Anomalies  : {anomalies}")

    # =====================================================
    # Update Prometheus Metrics
    # =====================================================

    TOTAL_PODS.set(total)
    NORMAL_PODS.set(normal)
    SUSPICIOUS_PODS.set(suspicious)
    HIGH_CONFIDENCE_ANOMALIES.set(anomalies)

    logger.info(
        f"Pods={total} | "
        f"Collecting={collecting} | "
        f"Normal={normal} | "
        f"Suspicious={suspicious} | "
        f"Anomalies={anomalies}"
    )

    # =====================================================
    # Recommendation Engine
    # =====================================================

    anomaly_df = live_metrics[
        live_metrics["Decision"] == "HIGH_CONFIDENCE_ANOMALY"
    ].copy()

    if anomaly_df.empty:

        print("\nNo high confidence anomalies detected.")

        logger.info("No high confidence anomalies detected.")

        return

    logger.warning(
        f"{len(anomaly_df)} high confidence anomalies detected."
    )

    actions = anomaly_df.apply(
        recommend_action,
        axis=1,
        result_type="expand"
    )

    anomaly_df["Recommended_Action"] = actions[0]
    anomaly_df["Reason"] = actions[1]

    print("\n")
    print("=" * 60)
    print("Recommended Actions")
    print("=" * 60)

    print(
        anomaly_df[
            [
                "Pod",
                "Decision",
                "CPU",
                "Memory_MB",
                "Recommended_Action",
                "Reason"
            ]
        ]
    )

    from datetime import datetime
    import os

    os.makedirs("monitoring/reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report_path = (
        f"monitoring/reports/anomaly_report_{timestamp}.csv"
    )

    anomaly_df.to_csv(
        report_path,
        index=False
    )

    logger.info(
        f"Anomaly report written to {report_path}"
    )

    # =====================================================
    # Self-Healing
    # =====================================================

    print("\n")
    print("=" * 60)
    print("Self-Healing Engine")
    print("=" * 60)

    for _, row in anomaly_df.iterrows():

        pod = row["Pod"]

        action = row["Recommended_Action"]

        logger.warning(
            "\n"
            "================ ANOMALY DETECTED ================\n"
            f"Pod                 : {pod}\n"
            f"Decision            : {row['Decision']}\n"
            f"CPU                 : {row['CPU']:.6f}\n"
            f"Memory              : {row['Memory_MB']:.2f} MB\n"
            f"ReconstructionError : {row['ReconstructionError']:.6f}\n"
            f"Recommended Action  : {action}\n"
            f"Reason              : {row['Reason']}\n"
            "=================================================="
        )

        if action == "Restart Pod":

            print(f"\nRestarting {pod}")

            restart_pod(pod)

        else:

            print(f"\nNo automatic remediation for {pod}")

            print(f"Recommended : {action}")

            print(f"Reason      : {row['Reason']}")

# =====================================================
# Main
# =====================================================

def main():

    logger.info(
        "Hybrid AIOps Monitoring Service Started."
    )

    start_http_server(8000)

    logger.info(
        "Prometheus metrics available at http://localhost:8000/metrics"
    )

    while True:

        detect_and_remediate()

        print(
            f"\nWaiting {CHECK_INTERVAL} seconds...\n"
        )

        logger.info(
            f"Sleeping {CHECK_INTERVAL} seconds."
        )

        time.sleep(CHECK_INTERVAL)


# =====================================================
# Entry Point
# =====================================================

if __name__ == "__main__":

    main()