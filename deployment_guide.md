# 🚀 Deployment Guide for Fund Administration Platform

## Overview
This guide provides step-by-step instructions for deploying the Fund Administration Workstream Management Platform to various cloud platforms.

## 1. Streamlit Cloud (Recommended)

### Prerequisites
- GitHub repository with your code
- Streamlit Cloud account

### Steps
1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository
   - Set main file path: `streamlit_app.py`
   - Deploy

### Configuration
```toml
# .streamlit/config.toml
[server]
headless = true
enableCORS = false
port = 8501

[browser]
gatherUsageStats = false
```

## 2. Heroku Deployment

### Prerequisites
- Heroku CLI installed
- Heroku account

### Steps
1. **Login to Heroku**
   ```bash
   heroku login
   ```

2. **Create Heroku app**
   ```bash
   heroku create your-fund-admin-app
   ```

3. **Deploy**
   ```bash
   git add .
   git commit -m "Heroku deployment"
   git push heroku main
   ```

4. **Open app**
   ```bash
   heroku open
   ```

## 3. Docker Deployment

### Local Development
```bash
# Build and run locally
docker-compose up --build

# Access at http://localhost:8501
```

### Production Deployment
```bash
# Build image
docker build -t fund-admin-app .

# Run container
docker run -p 8501:8501 fund-admin-app
```

## 4. AWS Deployment

### Option A: AWS App Runner
1. **Create Docker image**
   ```bash
   docker build -t fund-admin-app .
   ```

2. **Push to ECR**
   ```bash
   aws ecr create-repository --repository-name fund-admin-app
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
   docker tag fund-admin-app:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/fund-admin-app:latest
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/fund-admin-app:latest
   ```

3. **Deploy to App Runner**
   - Use AWS Console or CLI
   - Select ECR image
   - Configure port 8501

### Option B: AWS ECS
1. **Create ECS cluster**
2. **Create task definition**
3. **Deploy service**

## 5. Google Cloud Platform

### Option A: Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT-ID/fund-admin-app
gcloud run deploy fund-admin-app --image gcr.io/PROJECT-ID/fund-admin-app --platform managed --port 8501
```

### Option B: App Engine
1. **Create app.yaml**
   ```yaml
   runtime: python311
   entrypoint: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Deploy**
   ```bash
   gcloud app deploy
   ```

## 6. Azure Deployment

### Option A: Azure Container Instances
```bash
# Build and push to Azure Container Registry
az acr build --registry <registry-name> --image fund-admin-app .
az container create --resource-group <rg-name> --name fund-admin-app --image <registry-name>.azurecr.io/fund-admin-app:latest --ports 8501
```

### Option B: Azure App Service
1. **Create App Service**
2. **Configure for Python**
3. **Deploy via Azure CLI or GitHub Actions**

## Environment Variables

### Required
```bash
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### Optional
```bash
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
STREAMLIT_SERVER_ENABLE_CORS=false
STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
```

## Monitoring and Logging

### Health Checks
- Endpoint: `/_stcore/health`
- Expected response: `{"status": "healthy"}`

### Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Security Considerations

1. **Environment Variables**: Store sensitive data in environment variables
2. **HTTPS**: Enable SSL/TLS in production
3. **Authentication**: Consider adding authentication layer
4. **Rate Limiting**: Implement rate limiting for API endpoints

## Performance Optimization

1. **Caching**: Use Redis for session storage
2. **CDN**: Use CloudFront or similar for static assets
3. **Database**: Consider using managed database services
4. **Scaling**: Configure auto-scaling based on CPU/memory usage

## Troubleshooting

### Common Issues
1. **Port conflicts**: Ensure port 8501 is available
2. **Memory issues**: Increase container memory limits
3. **Timeout errors**: Increase timeout settings
4. **Import errors**: Check all dependencies are installed

### Debug Commands
```bash
# Check logs
docker logs <container-id>

# Access container shell
docker exec -it <container-id> /bin/bash

# Check health
curl http://localhost:8501/_stcore/health
``` 