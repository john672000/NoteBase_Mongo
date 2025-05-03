FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install necessary SSL-related packages
RUN apt-get update && \
    apt-get install -y ca-certificates openssl curl && \
    update-ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose FastAPI port
EXPOSE 8050

# Start FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8050"]