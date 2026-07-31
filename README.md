# 🤖 AIOps Framework for Autonomous Failure Detection and Remediation

An AI-powered AIOps framework that monitors Kubernetes workloads, detects anomalies using Machine Learning, predicts failures, and performs automated remediation.

---

## 📌 Project Overview

Modern cloud-native applications generate thousands of metrics every second. Detecting failures manually is slow and inefficient.

This project builds an intelligent AIOps platform capable of:

- Monitoring Kubernetes clusters
- Collecting real-time Prometheus metrics
- Detecting anomalies using Machine Learning
- Predicting failures using Deep Learning
- Automatically remediating failures
- Visualizing cluster health through dashboards

---

## 🏗️ System Architecture

```text
                   +----------------------+
                   |   Robot Shop App     |
                   +----------+-----------+
                              |
                              |
                              ▼
                     Kubernetes Cluster
                              |
                              ▼
                        Prometheus Server
                              |
                              ▼
                     Metrics Collector
                              |
                              ▼
                     Dataset Generation
                              |
                              ▼
                    Isolation Forest Model
                              |
                              ▼
                        LSTM Predictor
                              |
                              ▼
                    Remediation Engine
                              |
                              ▼
             Restart / Scale / Recover Pods
                              |
                              ▼
                    Monitoring Dashboard
```

---

# 🚀 Features

- Kubernetes Monitoring
- Prometheus Metrics Collection
- Grafana Dashboard
- Chaos Engineering using Chaos Mesh
- CPU Stress Injection
- Memory Stress Injection
- Network Delay Injection
- Pod Failure Simulation
- Dataset Generation
- Data Preprocessing
- Isolation Forest for Anomaly Detection *(Upcoming)*
- LSTM-based Failure Prediction *(Upcoming)*
- Automated Remediation *(Upcoming)*

---

# 🛠 Tech Stack

## Cloud

- Google Cloud Platform (GCP)
- Google Kubernetes Engine (GKE)

## Containerization

- Docker
- Kubernetes

## Monitoring

- Prometheus
- Grafana

## Chaos Engineering

- Chaos Mesh

## Machine Learning

- Python
- Pandas
- Scikit-learn
- Isolation Forest
- TensorFlow / Keras (LSTM)

---

# 📂 Project Structure

```text
aiops-project/

├── chaos/
│   ├── cpu-stress.yaml
│   ├── memory-stress.yaml
│   ├── network-delay.yaml
│   └── pod-kill.yaml
│
├── dashboard/
│
├── docs/
│
├── kubernetes/
│
├── models/
│
├── monitoring/
│   ├── metrics_collector.py
│   ├── preprocess_data.py
│
├── robot-shop/
│
├── README.md
└── requirements.txt
```

---

# 📊 Monitoring Pipeline

The metrics collector fetches Kubernetes metrics from Prometheus every 30 seconds.

Collected Metrics:

- CPU Usage
- Memory Usage
- Network RX
- Network TX
- Pod Status

The collected metrics are stored in a dataset for Machine Learning.

---

# 🌪 Chaos Engineering

The project simulates production failures using Chaos Mesh.

Implemented Experiments:

- CPU Stress
- Memory Stress
- Network Delay
- Pod Kill

These experiments generate realistic anomalies for training and validating the anomaly detection model.

---

# 🤖 Machine Learning Pipeline

## Phase 1

Isolation Forest

Purpose:

- Detect abnormal resource utilization
- Identify anomalous pods
- Real-time anomaly detection

---

## Phase 2

LSTM Network

Purpose:

- Learn workload patterns
- Predict future failures
- Early warning system

---

# 🔄 Workflow

```text
Robot Shop
      │
      ▼
Prometheus
      │
      ▼
Metrics Collector
      │
      ▼
Dataset
      │
      ▼
Isolation Forest
      │
      ▼
LSTM Predictor
      │
      ▼
Remediation Engine
      │
      ▼
Restart / Scale Pods
```

---

# 📸 Screenshots

Screenshots will be added for:

- Robot Shop
- Kubernetes Cluster
- Grafana Dashboard
- Prometheus
- Chaos Mesh
- Anomaly Detection Dashboard

---

# 📈 Current Progress

- [x] Kubernetes Deployment
- [x] Robot Shop Deployment
- [x] Prometheus Setup
- [x] Grafana Setup
- [x] Metrics Collection
- [x] Chaos Engineering
- [x] Dataset Collection
- [x] Dataset Preprocessing
- [ ] Isolation Forest
- [ ] LSTM Prediction
- [ ] Automated Remediation
- [ ] Dashboard Integration

---

# 👨‍💻 Author

**Satwik Singh**

Information Science & Engineering

RNS Institute of Technology

---

# ⭐ Future Improvements

- Explainable AI (XAI)
- Root Cause Analysis
- Reinforcement Learning-based Self-Healing
- Multi-cluster Monitoring
- Slack/Email Alerts
- Kubernetes Operator for Automated Recovery

---

## ⭐ If you like this project, don't forget to star the repository!