@echo off
echo Applying CPU Stress...
kubectl apply -f chaos\cpu-stress.yaml
kubectl get stresschaos -n chaos-mesh
pause