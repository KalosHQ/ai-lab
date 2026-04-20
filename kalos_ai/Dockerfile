# Kalos AI - Dockerfile for Production Deployment
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (git + GL libs required for trimesh/smplx)
RUN apt-get update && apt-get install -y \
    git \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install torch and torchvision separately (CPU only, much smaller)
RUN pip install --no-cache-dir --timeout=300 \
    torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Install remaining dependencies
RUN pip install --no-cache-dir --timeout=300 -r requirements.txt

# Copy the application code
COPY . .

# Create output directory
RUN mkdir -p output

# Set environment variables
ENV PYTHONPATH=/app
ENV SMPLX_MODEL_DIR=/app/models/smplx
ENV SMPLX_OUTPUT_DIR=/app/output

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run the application with gunicorn + uvicorn workers for production
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "src.api.main:app", "--bind", "0.0.0.0:8000"]
