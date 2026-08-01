@echo off

echo ===============================
echo Robot Shop Pods
echo ===============================

kubectl get pods -n robot-shop

echo.

echo ===============================
echo Monitoring Pods
echo ===============================

kubectl get pods -n monitoring

echo.

echo ===============================
echo Chaos Mesh
echo ===============================

kubectl get pods -n chaos-mesh

echo.

echo ===============================
echo Nodes
echo ===============================

kubectl get nodes

pause