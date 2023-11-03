# Use Node.js as base image
FROM node:14

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install app dependencies
RUN npm install

# Copy app source to container
COPY . /app

EXPOSE 3000

# Start the app
CMD ["npm", "start"]
