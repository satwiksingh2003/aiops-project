@echo off
title Prometheus Port Forward

cd /d %~dp0..

kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9090:9090

pause