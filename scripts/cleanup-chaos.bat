@echo off
echo Removing Chaos Experiments...

kubectl delete -f chaos\cpu-stress.yaml
kubectl delete -f chaos\memory-stress.yaml
kubectl delete -f chaos\network-delay.yaml
kubectl delete -f chaos\pod-kill.yaml

echo.
echo Cleanup Complete.

pause