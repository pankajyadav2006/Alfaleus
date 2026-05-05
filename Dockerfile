FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create directory for SQLite database if it doesn't exist
# Note: In production, this should be a persistent volume mount
RUN mkdir -p /app/data

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV ANTHROPIC_API_KEY=""

# Expose port
EXPOSE 8000

# Command to run the application
# We use --host 0.0.0.0 for deployment
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
