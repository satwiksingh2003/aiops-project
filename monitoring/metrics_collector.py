import requests
import pandas as pd
from datetime import datetime
import os
import time

# Prometheus API URL
import os

PROMETHEUS_URL = os.getenv(
    "PROMETHEUS_URL",
    "http://localhost:9090/api/v1/query"
)

# -------------------------------------------------
# Query Prometheus
# -------------------------------------------------
def query_prometheus(promql_query):
    """
    Sends a PromQL query to Prometheus and returns the JSON response.
    """

    response = requests.get(
        PROMETHEUS_URL,
        params={"query": promql_query}
    )

    response.raise_for_status()

    return response.json()


# -------------------------------------------------
# Generic Metric Builder
# -------------------------------------------------
def build_metric_dictionary(result, conversion_factor=1):
    """
    Converts a Prometheus metric into a dictionary.

    Returns:
    {
        pod_name : metric_value
    }
    """

    metric_data = {}

    for item in result["data"]["result"]:

        pod_name = item["metric"]["pod"]

        metric_value = float(item["value"][1]) / conversion_factor

        metric_data[pod_name] = metric_value

    return metric_data


# -------------------------------------------------
# Pod Status Builder
# -------------------------------------------------
def build_status_dictionary(result):
    """
    Converts pod status query into a dictionary.
    """

    status_data = {}

    for item in result["data"]["result"]:

        pod_name = item["metric"]["pod"]

        status = int(float(item["value"][1]))

        status_data[pod_name] = status

    return status_data


# -------------------------------------------------
# Collect Metrics
# -------------------------------------------------
def collect_metrics():

    # CPU
    cpu_query = '''
    sum(rate(container_cpu_usage_seconds_total{
        namespace="robot-shop",
        container!=""
    }[1m])) by (pod)
    '''

    # Memory
    memory_query = '''
    sum(container_memory_working_set_bytes{
        namespace="robot-shop",
        container!=""
    }) by (pod)
    '''

    # Network RX
    network_rx_query = '''
    sum(rate(container_network_receive_bytes_total{
        namespace="robot-shop"
    }[1m])) by (pod)
    '''

    # Network TX
    network_tx_query = '''
    sum(rate(container_network_transmit_bytes_total{
        namespace="robot-shop"
    }[1m])) by (pod)
    '''

    # Pod Status
    pod_status_query = '''
    kube_pod_status_phase{
        namespace="robot-shop",
        phase="Running"
    }
    '''

    # Fetch Results
    cpu_result = query_prometheus(cpu_query)
    memory_result = query_prometheus(memory_query)
    network_rx_result = query_prometheus(network_rx_query)
    network_tx_result = query_prometheus(network_tx_query)
    pod_status_result = query_prometheus(pod_status_query)

    # Build Dictionaries
    memory_data = build_metric_dictionary(
        memory_result,
        1024 * 1024
    )

    network_rx_data = build_metric_dictionary(
        network_rx_result,
        1024
    )

    network_tx_data = build_metric_dictionary(
        network_tx_result,
        1024
    )

    pod_status_data = build_status_dictionary(
        pod_status_result
    )

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rows = []

    # Merge all metrics
    for item in cpu_result["data"]["result"]:

        pod_name = item["metric"]["pod"]

        rows.append({

            "Timestamp": current_time,

            "Pod": pod_name,

            "CPU": round(float(item["value"][1]), 6),

            "Memory_MB":
                round(memory_data.get(pod_name, 0), 2),

            "Network_RX_KBps":
                round(network_rx_data.get(pod_name, 0), 3),

            "Network_TX_KBps":
                round(network_tx_data.get(pod_name, 0), 3),

            "Pod_Status":
                pod_status_data.get(pod_name, 0)

        })

    return pd.DataFrame(rows)


# -------------------------------------------------
# Save CSV
# -------------------------------------------------
def save_to_csv(df):

    csv_file = "monitoring/dataset.csv"

    file_exists = os.path.isfile(csv_file)

    df.to_csv(
        csv_file,
        mode="a",
        header=not file_exists,
        index=False
    )

    print(f"\n{len(df)} rows added to {csv_file}")


# -------------------------------------------------
# Main
# -------------------------------------------------
def main():

    print("=" * 60)
    print("AIOps Monitoring Collector Started")
    print("=" * 60)

    while True:

        try:

            df = collect_metrics()

            print("\nCollected Metrics:\n")
            print(df)

            save_to_csv(df)

        except Exception as e:

            print("\nCollection failed.")
            print(e)

        print("\nWaiting for 30 seconds...\n")

        time.sleep(30)


if __name__ == "__main__":
    main()