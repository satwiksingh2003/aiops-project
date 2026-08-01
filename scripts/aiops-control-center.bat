@echo off
title AIOps Control Center
color 0A

:MENU
cls

echo.
echo ============================================================
echo                     AIOps CONTROL CENTER
echo ============================================================
echo.
echo   PROJECT : Autonomous Failure Detection ^& Remediation
echo   CLUSTER : aiops-cluster
echo   STATUS  : Ready
echo.
echo ============================================================
echo.
echo   [1]  Start Entire Project
echo   [2]  Check Cluster Health
echo   [3]  Open Robot Shop
echo   [4]  Open Grafana
echo   [5]  Open Prometheus
echo.
echo ---------------------- CHAOS TESTING ------------------------
echo.
echo   [6]  CPU Stress
echo   [7]  Memory Stress
echo   [8]  Network Delay
echo   [9]  Pod Kill
echo   [10] Cleanup Chaos
echo.
echo ----------------------- UTILITIES ---------------------------
echo.
echo   [11] Stop Port Forwarding
echo   [12] Exit
echo.
echo ============================================================

set /p choice=Enter your choice :

if "%choice%"=="1" call start-project.bat
if "%choice%"=="2" call check-cluster.bat
if "%choice%"=="3" start http://34.100.171.210:8080
if "%choice%"=="4" start http://localhost:3000
if "%choice%"=="5" start http://localhost:9090
if "%choice%"=="6" call cpu-stress.bat
if "%choice%"=="7" call memory-stress.bat
if "%choice%"=="8" call network-delay.bat
if "%choice%"=="9" call pod-kill.bat
if "%choice%"=="10" call cleanup-chaos.bat
if "%choice%"=="11" call stop-portforward.bat
if "%choice%"=="12" exit

goto MENU