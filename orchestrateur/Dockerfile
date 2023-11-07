# Use an official Python runtime as the parent image
FROM python:3.10-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org --no-cache-dir -r requirements.txt


# Make port 5000 available to the world outside this container
EXPOSE 5001

# Define environment variable if needed (e.g., setting a Flask environment variable)
# ENV FLASK_ENV=production

# Run app.py when the container launches
CMD ["python", "app.py"]