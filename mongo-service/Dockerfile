# Use the official MongoDB image
FROM mongo:latest

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Start MongoDB and the Flask app using a script
CMD ["sh", "-c", "mongod --fork --logpath /var/log/mongod.log; python3 mongo.py"]
