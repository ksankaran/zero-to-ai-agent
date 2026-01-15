# From: Zero to AI Agent, Chapter 19, Section 19.3
# File: DEPLOYMENT.md (Exercise 3 Solution)

# Deployment Guide

This guide explains how to deploy the Agent API to production.

## Prerequisites

Before deploying, ensure you have:

1. **A GitHub account** with this repository pushed to it
2. **An OpenAI API key** from https://platform.openai.com/api-keys
3. **A Railway account** (or your preferred platform) at https://railway.com

## Environment Variables

The following environment variables must be configured:

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | Your OpenAI API key for LLM access |
| `API_KEY` | No | Authentication key for the API (default: dev-key-change-in-production) |
| `DEBUG` | No | Enable debug mode (default: false) |
| `LOG_LEVEL` | No | Logging verbosity: DEBUG, INFO, WARNING, ERROR (default: INFO) |
| `PORT` | No | Port to run the server on (default: 8000, often set by platform) |
| `MODEL_NAME` | No | OpenAI model to use (default: gpt-3.5-turbo) |
| `MAX_TOKENS` | No | Maximum tokens per response (default: 1000) |

⚠️ **Security Note**: Never commit actual API keys to the repository. Always use the platform's secret management.

## Deployment Steps

### Option 1: Railway (Recommended for Beginners)

1. **Connect Repository**
   - Log in to Railway at railway.com
   - Click "New Project"
   - Select "GitHub Repo" from the list of sources
   - Select this repository
   - Railway will detect the Dockerfile automatically

2. **Configure Environment Variables**
   - Click on your service
   - Go to "Variables" tab
   - Add each required environment variable
   - Click "Deploy" in the "Apply changes" toast at the top

3. **Generate Public URL**
   - Go to "Settings" tab
   - Scroll to "Networking" section
   - Click "Generate Domain" under "Public Networking"
   - Note your public URL (e.g., `your-app.up.railway.app`)

4. **Verify Deployment**
   - Check the "Deployments" tab for build status
   - Once deployed, test with the verification steps below

### Option 2: Render

1. **Create Web Service**
   - Log in to Render
   - Click "New" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service**
   - Environment: Docker
   - Add environment variables in the "Environment" section

3. **Deploy**
   - Click "Create Web Service"
   - Wait for the build to complete

### Option 3: Manual Docker Deployment

If deploying to your own server:

```bash
# Build the image
docker build -f Dockerfile.deploy -t agent-api:latest .

# Run with environment variables
docker run -d \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your-key \
  -e API_KEY=your-api-key \
  --name agent-api \
  agent-api:latest
```

## Verifying the Deployment

After deployment, verify everything is working:

### 1. Health Check

```bash
curl https://your-domain.com/health
```

Expected response:
```json
{"status": "healthy", "version": "1.0.0"}
```

### 2. API Documentation

Visit `https://your-domain.com/docs` in your browser. You should see the interactive Swagger documentation.

### 3. Test Chat Endpoint

```bash
curl -X POST "https://your-domain.com/v1/chat" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your-api-key" \
     -d '{"message": "Hello, are you working?"}'
```

Expected response:
```json
{
  "response": "Hello! Yes, I'm working...",
  "conversation_id": "...",
  "processing_time_ms": ...
}
```

## Rollback Procedure

If a deployment causes issues:

### Railway
1. Go to "Deployments" tab
2. Find the last working deployment
3. Click the three dots menu → "Rollback"

### Render
1. Go to "Events" tab
2. Find the last successful deploy
3. Click "Rollback to this deploy"

### Manual Verification After Rollback
Always verify the rollback succeeded:
```bash
curl https://your-domain.com/health
```

## Monitoring

After deployment, monitor your application:

1. **Logs**: Check platform logs for errors
2. **Health endpoint**: Set up uptime monitoring on `/health`
3. **Error rates**: Watch for 5xx responses

## Troubleshooting

### Build Fails
- Check build logs for specific errors
- Verify all dependencies are in requirements.txt
- Ensure Dockerfile syntax is correct

### App Crashes on Startup
- Verify all required environment variables are set
- Check logs for missing configuration errors
- Test locally with same environment variables

### Requests Timeout
- Check if the app is binding to 0.0.0.0 (not 127.0.0.1)
- Verify PORT environment variable is used
- Check platform-specific port requirements

### 500 Errors
- Check application logs for stack traces
- Verify OPENAI_API_KEY is valid
- Check OpenAI API status at status.openai.com

## Support

For issues with:
- **This application**: Open a GitHub issue
- **Railway**: https://docs.railway.app
- **Render**: https://render.com/docs
- **OpenAI API**: https://help.openai.com
