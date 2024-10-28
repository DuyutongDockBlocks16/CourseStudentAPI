kubectl apply -f persistent-volume.yaml
kubectl apply -f mongo.yaml
kubectl apply -f fastapi.yaml

kubectl port-forward service/fast-api-service 5000:5000
kubectl port-forward service/mongo 31048:27017

eval $(minikube -p minikube docker-env)
docker build -t fast-api-backend:v1 .
vim ~/.docker/config.json
minikube start
minikube profile list
minikube ssh