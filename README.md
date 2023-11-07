# CloudProjectDockerWatson

# * Chat Bot PORT 5000*
First Point to the ibm-chatbot-service directory <br />
cd /ibm-chatbot-service

# ! If you don't have the redis docker image
docker pull redis

# To run the redis databse locally
docker run -d -p 6379:6379 --name redis-container redis 
# Run redis command line
docker exec -it my-redis-container redis-cli
# To see all stored keys from cli
KEYS *
# To see stored key content from cli
GET [keyname]

# Run the chatbot service
py app.py

# Run it as docker instance 
Point on folder with cd <br />
Build the docker image <br />
docker build -t chatbot-service .

# Run the image
docker run -d 5000:5000 --name chatbot-service

# Puch to registry 
First connect to the cloud registry ( You have to install aws cli on windows ) <br />
aws configure

# Build the image  
docker build -t 448878779811.dkr.ecr.eu-west-3.amazonaws.com/acospain-ecr:groupe6-watson .

# Tag the image 
docker tag 448878779811.dkr.ecr.eu-west-3.amazonaws.com/acospain-ecr:groupe6-watson 448878779811.dkr.ecr.eu-west-3.amazonaws.com/acospain-ecr:groupe6-watson

# Push the image
docker push 448878779811.dkr.ecr.eu-west-3.amazonaws.com/acospain-ecr:groupe6-watson

# * Docker Compose *

No more need to run docker images separatly you can use first time build :</br>

docker-compose up --build

Later on :

docker-compose up

# * Kubernetees *
# Install minikube for local kubernetees
minikube start --driver=docker

# To check the status of pods:
kubectl get pods -n chatbot-namespace
#check services
kubectl get services -n chatbot-namespace



# Access services
kubectl port-forward -n chatbot-namespace service/chatbot-front-service 3000:3000

# Clean up ( Remove everything)
kubectl delete -f chatbot-namespace.yaml


# push to aws
aws ecr get-login-password --region eu-west-3 | docker login --username AWS --password-stdin 448878779811.dkr.ecr.eu-west-3.amazonaws.com
docker build -t team6-front:latest -t 448878779811.dkr.ecr.eu-west-3.amazonaws.com/acospain-ecr:team6-front .
docker build -t team6-api -t 448878779811.dkr.ecr.eu-west-3.amazonaws.com/acospain-ecr:team6-api .
docker build -t team6-orchestrateur -t 448878779811.dkr.ecr.eu-west-3.amazonaws.com/acospain-ecr:team6-orchestrateur . 
docker build -t redis -t 448878779811.dkr.ecr.eu-west-3.amazonaws.com/acospain-ecr:team6-redis .

docker tag team6-front 448878779811.dkr.ecr.eu-west-3.amazonaws.com/acospain-ecr:team6-front
docker tag team6-api 448878779811.dkr.ecr.eu-west-3.amazonaws.com/acospain-ecr:team6-api
docker tag team6-orchestrateur 448878779811.dkr.ecr.eu-west-3.amazonaws.com/acospain-ecr:team6-orchestrateur
docker tag redis 448878779811.dkr.ecr.eu-west-3.amazonaws.com/acospain-ecr:team6-redis

docker push 448878779811.dkr.ecr.eu-west-3.amazonaws.com/acospain-ecr:team6-front
docker push 448878779811.dkr.ecr.eu-west-3.amazonaws.com/acospain-ecr:team6-api
docker push 448878779811.dkr.ecr.eu-west-3.amazonaws.com/acospain-ecr:team6-orchestrateur
docker push 448878779811.dkr.ecr.eu-west-3.amazonaws.com/acospain-ecr:team6-redis


kubectl apply -f api-deployment.yaml
kubectl apply -f frontend-deployment.yaml
kubectl apply -f orchestrateur-deployment.yaml
kubectl apply -f redis-deployment.yaml

 kubectl apply -f api-service.yaml
  kubectl apply -f frontend-service.yaml
   kubectl apply -f orchestrateur-service.yaml
   kubectl apply -f redis-service.yaml

    kubectl apply -f ingress.yaml

