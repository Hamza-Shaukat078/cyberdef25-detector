# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Create input and output directories
RUN mkdir -p /input/logs /output

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY model.pkl .
COPY feature_names.txt .
COPY inference.py .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the inference script
CMD ["python", "inference.py"]
