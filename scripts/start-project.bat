@echo off
title AIOps Project Startup
color 0A

echo ==========================================
echo        AIOps Project Startup
echo ==========================================

REM ==========================================
REM Go to Project Root
REM ==========================================
cd /d %~dp0..

REM ==========================================
REM Load Configuration
REM ==========================================
call scripts\config.bat

echo.
echo Connecting to GKE Cluster...
call gcloud container clusters get-credentials %CLUSTER_NAME% --zone %CLUSTER_ZONE% --project %PROJECT_ID%

if %ERRORLEVEL% neq 0 (
    echo.
    echo ERROR: Failed to connect to the GKE cluster.
    pause
    exit /b
)

echo.
echo ==========================================
echo Cluster Connected Successfully!
echo ==========================================

echo.
echo Checking Cluster Nodes...
kubectl get nodes

echo.
echo Checking Monitoring Pods...
kubectl get pods -n monitoring

echo.
echo ==========================================
echo Starting Grafana Port Forward...
echo ==========================================
start "Grafana" cmd /k "kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80"

echo.
echo ==========================================
echo Starting Prometheus Port Forward...
echo ==========================================
start "Prometheus" cmd /k "kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9090:9090"

echo.
echo Waiting for services to start...
timeout /t 5 >nul

echo.
echo Opening Robot Shop...
start http://34.100.171.210:8080

echo Opening Grafana...
start http://localhost:3000

echo Opening Prometheus...
start http://localhost:9090

echo.
echo ==========================================
echo          Project Ready!
echo ==========================================
echo.
echo Services:
echo ------------------------------------------
echo Robot Shop : http://34.100.171.210:8080
echo Grafana    : http://localhost:3000
echo Prometheus : http://localhost:9090
echo ------------------------------------------
echo.
echo NOTE:
echo Keep the Grafana and Prometheus command
echo windows OPEN. They are running the
echo kubectl port-forward commands.
echo.
echo Happy Monitoring!
echo ==========================================

pause