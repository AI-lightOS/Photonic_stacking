# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Install the package in editable mode for local development
RUN pip install -e .

# Set environment variables
ENV PYTHONPATH="/app"

# Metadata
LABEL maintainer="LightRail AI Team"
LABEL architecture="Universal XPU"

# Default command
ENTRYPOINT ["python", "-m", "lightcompiler.compiler_v2"]
CMD ["--help"]
