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

# * SpeechToText PORT 5001* 
# Run it as docker instance 
Point on folder with cd <br />
Build the docker image <br />
docker build -t chatbot-service .
# Run the image
docker run speechtext -d 5001:5001 --name speechtext

# * Compose *

No more need to run docker images separatly you can use first time build :</br>

docker-compose up --build

Later on :

docker-compose up

