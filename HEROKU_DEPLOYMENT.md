# 🚀 Heroku Deployment Guide for Fund Administration Platform

## Prerequisites
- Heroku account (you have this)
- Git installed
- Python 3.11+ installed

## Method 1: Using Heroku CLI (Recommended)

### Step 1: Install Heroku CLI
```bash
# Windows (using winget)
winget install --id=Heroku.HerokuCLI -e

# Or download from: https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Login to Heroku
```bash
heroku login
```

### Step 3: Initialize Git (if not already done)
```bash
git init
git add .
git commit -m "Initial commit for Heroku deployment"
```

### Step 4: Create Heroku App
```bash
heroku create your-fund-admin-app
```

### Step 5: Deploy
```bash
git push heroku main
```

### Step 6: Open the App
```bash
heroku open
```

## Method 2: Using Heroku Dashboard (Alternative)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Prepare for Heroku deployment"
git push origin main
```

### Step 2: Connect to Heroku Dashboard
1. Go to [Heroku Dashboard](https://dashboard.heroku.com)
2. Click "New" → "Create new app"
3. Choose app name: `your-fund-admin-app`
4. Select region
5. Click "Create app"

### Step 3: Connect GitHub Repository
1. In your app dashboard, go to "Deploy" tab
2. Under "Deployment method", select "GitHub"
3. Connect your GitHub account
4. Select your repository: `OCR-app-1`
5. Click "Connect"

### Step 4: Configure Buildpacks
1. Go to "Settings" tab
2. Click "Add buildpack"
3. Add: `heroku/python`

### Step 5: Deploy
1. Go back to "Deploy" tab
2. Under "Manual deploy", click "Deploy Branch"
3. Wait for deployment to complete

## Configuration Files Created

### 1. Procfile
```
web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
```

### 2. runtime.txt
```
python-3.11.7
```

### 3. requirements.txt
Updated with all necessary dependencies including gunicorn

### 4. .streamlit/config.toml
Streamlit configuration for production deployment

## Environment Variables

Set these in Heroku Dashboard → Settings → Config Vars:

```
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

## Troubleshooting

### Common Issues:

1. **Build Fails**
   - Check requirements.txt for version conflicts
   - Ensure all dependencies are compatible

2. **App Crashes**
   - Check logs: `heroku logs --tail`
   - Verify Procfile is correct
   - Check environment variables

3. **Port Issues**
   - Heroku assigns port via $PORT environment variable
   - Ensure app uses `$PORT` not hardcoded port

### Debug Commands:
```bash
# View logs
heroku logs --tail

# Check app status
heroku ps

# Restart app
heroku restart

# Run one-off dyno for debugging
heroku run python -c "import streamlit; print('Streamlit version:', streamlit.__version__)"
```

## Post-Deployment

### 1. Verify Deployment
- Visit your app URL
- Test all major features
- Check for any errors in logs

### 2. Set Up Monitoring
- Enable Heroku add-ons for monitoring
- Set up log aggregation if needed

### 3. Scale (if needed)
```bash
# Scale to 2 dynos
heroku ps:scale web=2

# Check current dynos
heroku ps
```

## Cost Optimization

### Free Tier (No longer available)
- Heroku removed free tier in 2022
- Basic dyno: $7/month

### Hobby Dyno ($7/month)
- 512MB RAM
- Shared CPU
- Sleep after 30 minutes of inactivity

### Standard Dyno ($25/month)
- 1GB RAM
- Dedicated CPU
- No sleep

## Security Considerations

1. **Environment Variables**: Store sensitive data in Heroku config vars
2. **HTTPS**: Automatically enabled on Heroku
3. **Authentication**: Consider adding authentication layer
4. **Rate Limiting**: Implement if needed

## Performance Tips

1. **Caching**: Use Redis add-on for session storage
2. **Optimization**: Monitor memory usage
3. **Scaling**: Scale dynos based on traffic
4. **CDN**: Consider using CloudFront for static assets

## Next Steps

After successful deployment:

1. **Domain Setup**: Add custom domain if needed
2. **SSL Certificate**: Automatically provided by Heroku
3. **Monitoring**: Set up alerts and monitoring
4. **Backup**: Implement data backup strategy
5. **CI/CD**: Set up automatic deployments from GitHub 