FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies including SSL certs
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates gcc && \
    rm -rf /var/lib/apt/lists/*
# Copy source code
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose FastAPI port
EXPOSE 8050

# Start FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8050"]
