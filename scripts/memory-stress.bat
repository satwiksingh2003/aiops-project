@echo off
echo Applying Memory Stress...
kubectl apply -f chaos\memory-stress.yaml
pause