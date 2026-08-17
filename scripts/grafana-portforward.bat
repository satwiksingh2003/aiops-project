@echo off
title Grafana Port Forward

cd /d %~dp0..

kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80

pause