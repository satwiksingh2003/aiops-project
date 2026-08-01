@echo off
echo Applying Network Delay...
kubectl apply -f chaos\network-delay.yaml
pause