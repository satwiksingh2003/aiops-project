@echo off
echo Killing Web Pod...
kubectl apply -f chaos\pod-kill.yaml
pause