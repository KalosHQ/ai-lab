# Kalos AI - Deployment Guide

This guide covers how to deploy the Kalos AI application in different environments.

## Prerequisites

### SMPL-X Models
The application requires SMPL-X model files to generate avatars. You must obtain these separately:

1. **Register at SMPL-X:** Go to https://smpl-x.is.tue.mpg.de/ and create an account
2. **Download models:** Download the SMPL-X model files (SMPLX_NEUTRAL.npz, SMPLX_MALE.npz, SMPLX_FEMALE.npz)
3. **Place models:** Put the files in a directory accessible to the application

## Deployment Options

### Option 1: Local Development

```bash
# 1. Clone the repository
cd ai-lab/kalos_ai

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up models directory
mkdir -p models/smplx
# Copy your SMPL-X .npz files to models/smplx/

# 5. Copy environment file
cp .env.example .env
# Edit .env with your configuration

# 6. Run the application
uvicorn src.api.main:app --reload --port 8000
```

Visit http://localhost:8000/docs for the API documentation.

### Option 2: Docker Deployment (Recommended for Production)

```bash
# 1. Build the Docker image
cd ai-lab/kalos_ai
docker build -t kalos-ai:latest .

# 2. Prepare models directory
mkdir -p /path/to/your/models/smplx
# Copy your SMPL-X .npz files to this directory

# 3. Run the container
docker run -d \
  -p 8000:8000 \
  -v /path/to/your/models/smplx:/app/models/smplx \
  -v /path/to/your/output:/app/output \
  --name kalos-ai \
  kalos-ai:latest

# 4. Check logs
docker logs kalos-ai
```

#### Docker with Environment Variables

```bash
docker run -d \
  -p 8000:8000 \
  -v /path/to/models:/app/models/smplx \
  -e SMPLX_MODEL_DIR=/app/models/smplx \
  -e SMPLX_OUTPUT_DIR=/app/output \
  --name kalos-ai \
  kalos-ai:latest
```

### Option 3: Google Colab

```python
# 1. Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# 2. Clone your repository
!git clone https://github.com/your-repo/kalos.git
%cd kalos/ai-lab/kalos_ai

# 3. Install dependencies
!pip install -r requirements.txt

# 4. Set up models path (adjust to your Drive path)
%env SMPLX_MODEL_DIR=/content/drive/MyDrive/models/smplx
%env SMPLX_OUTPUT_DIR=/content/drive/MyDrive/kalos_output

# 5. Run the server with ngrok for public access
!pip install pyngrok
from pyngrok import ngrok
import uvicorn
import threading

# Start ngrok tunnel
public_url = ngrok.connect(8000)
print(f"Public URL: {public_url}")

# Run the server in a background thread
def run_server():
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000)

threading.Thread(target=run_server).start()
```

### Option 4: Cloud Deployment (AWS/GCP/Azure)

#### AWS EC2

```bash
# 1. Launch an EC2 instance (Ubuntu 20.04+)
# 2. SSH into the instance
ssh -i your-key.pem ubuntu@your-instance-ip

# 3. Install Docker
sudo apt update
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker

# 4. Follow Docker deployment steps above

# 5. Configure security group to allow port 8000
```

#### Google Cloud Run

```bash
# 1. Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/your-project/kalos-ai

# 2. Deploy to Cloud Run
gcloud run deploy kalos-ai \
  --image gcr.io/your-project/kalos-ai \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 1
```

Note: Cloud Run has memory limitations. For SMPL-X models, consider using Cloud Run with larger memory or use a different service.

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SMPLX_MODEL_DIR` | Path to SMPL-X model files | `models/smplx` |
| `SMPLX_OUTPUT_DIR` | Path for output files | `output` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |

### Production Considerations

1. **Model Storage:** Store models in a persistent volume or cloud storage
2. **Output Storage:** Use cloud storage (S3, GCS) for generated avatars
3. **Security:** 
   - Update CORS settings in `main.py`
   - Add authentication
   - Use HTTPS
4. **Scaling:** Consider using a task queue (Celery) for long-running generation tasks
5. **Monitoring:** Add logging and health checks

## Troubleshooting

### Models Not Found
```
FileNotFoundError: SMPL-X model directory not found
```
**Solution:** Ensure models are in the correct directory and the path is set correctly.

### Permission Denied
```
PermissionError: [Errno 13] Permission denied
```
**Solution:** Check file permissions on the models and output directories.

### Memory Issues
```
Killed or Out of Memory
```
**Solution:** Increase container/server memory. SMPL-X models require ~1GB RAM.

## API Endpoints

- `GET /health` - Health check
- `POST /api/ai/generate-avatar` - Generate 3D avatar

## Support

For issues:
1. Check the logs: `docker logs kalos-ai`
2. Verify models are in the correct location
3. Check the `/health` endpoint for model loading status