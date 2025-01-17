# Use a slim Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt (if you have one)
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy Python script
COPY asr_api.py .

# Expose the port where the Flask app runs
EXPOSE 5000

# Define the command to run the Flask app and clean up the file 
CMD ["python", "asr_api.py" , "&", "rm", "asr_api.py"]