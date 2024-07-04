# Use an official Python runtime as a parent image
FROM python:3.10.14-slim

# Set the working directory in the container
WORKDIR /src

# Copy the current directory contents into the container at /src
COPY . /src

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9092
EXPOSE 29092

# Define environment variable
ENV NAME KafkaPythonApp

# Run the Python script when the container launches
CMD ["python", "./src/data_generator.py"]