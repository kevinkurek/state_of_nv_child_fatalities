# Start from Python 3.10 base image
FROM python:3.10-slim-buster

# Set working directory in the container
WORKDIR /app

# Copy the entire directory into the Docker container
COPY . /app

# Install pip requirements and tox
RUN pip install --no-cache-dir -r requirements.txt

# Run tox
RUN tox

# Set the flask application script as the default command for the container
# Flask will run on port 8080
ENV PORT 8080
CMD ["python", "flask_main.py"]
