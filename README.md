# CloudProjectDockerWatson

# * Chat Bot *
First Point to the ibm-chatbot-service directory
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
# Build the docker image
docker build -t chatbot-service .

# Run the image
docker run -d 5000:5000 --name chatbot-service

# Puch to registry 
First connect to the cloud registry ( You have to install aws cli on windows )
aws configure

# Build the image  
docker build -t 448878779811.dkr.ecr.eu-west-3.amazonaws.com/acospain-ecr:groupe6-watson .

# Tag the image 
docker tag 448878779811.dkr.ecr.eu-west-3.amazonaws.com/acospain-ecr:groupe6-watson 448878779811.dkr.ecr.eu-west-3.amazonaws.com/acospain-ecr:groupe6-watson

# Push the image
docker push 448878779811.dkr.ecr.eu-west-3.amazonaws.com/acospain-ecr:groupe6-watson


# FrontReact

Coming soon ...
 
