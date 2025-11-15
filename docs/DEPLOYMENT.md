# Deployment Guide

## Prerequisites

1. **Google Cloud Account** with billing enabled
2. **gcloud CLI** installed and configured
3. **API Keys** properly configured
4. **ADK** installed: `pip install google-adk`

---

## Method 1: Agent Engine Deployment (Recommended)

### Step 1: Prepare Project

```powershell
# Authenticate with Google Cloud
gcloud auth login
gcloud auth application-default login

# Set your project
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable run.googleapis.com
```

### Step 2: Configure Deployment

Verify `.agent_engine_config.json` exists:

```json
{
  "agent_id": "adaptive-chef",
  "display_name": "The Adaptive Chef",
  "model": "gemini-2.0-flash-exp",
  "region": "us-central1",
  "entry_point": "agent.py",
  "agent_name": "root_agent"
}
```

### Step 3: Store API Key as Secret

```powershell
# Create secret for API key
echo "your-actual-api-key" | gcloud secrets create google_api_key --data-file=-

# Grant access to Cloud Run service account
gcloud secrets add-iam-policy-binding google_api_key `
  --member="serviceAccount:YOUR_PROJECT_ID@appspot.gserviceaccount.com" `
  --role="roles/secretmanager.secretAccessor"
```

### Step 4: Deploy

```powershell
# Deploy to Agent Engine
adk deploy agent_engine `
  --project=YOUR_PROJECT_ID `
  --region=us-central1 `
  .

# Expected output:
# ✅ Agent deployed successfully!
# 🌐 Endpoint: https://us-central1-YOUR_PROJECT.cloudfunctions.net/adaptive-chef
```

### Step 5: Test Deployment

```powershell
# Test with curl
curl -X POST https://YOUR_REGION-YOUR_PROJECT.cloudfunctions.net/adaptive-chef `
  -H "Content-Type: application/json" `
  -d '{\"message\": \"I am vegan, add rice to my pantry\"}'
```

---

## Method 2: Cloud Run Deployment

### Step 1: Create Dockerfile

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080
ENV GOOGLE_API_KEY=${GOOGLE_API_KEY}

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
```

### Step 2: Create Flask Wrapper

Create `app.py`:

```python
from flask import Flask, request, jsonify
import asyncio
from agent import process_user_request

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    session_id = data.get('session_id', 'default')
    
    # Run async function
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response = loop.run_until_complete(
        process_user_request(user_input, session_id)
    )
    
    return jsonify({'response': response})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

### Step 3: Build and Deploy

```powershell
# Build container
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/adaptive-chef

# Deploy to Cloud Run
gcloud run deploy adaptive-chef `
  --image gcr.io/YOUR_PROJECT_ID/adaptive-chef `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars GOOGLE_API_KEY=your-key `
  --memory 2Gi `
  --cpu 2 `
  --timeout 300
```

---

## Method 3: Local Testing with Docker

### Build Image

```powershell
docker build -t adaptive-chef:local .
```

### Run Container

```powershell
docker run -p 8080:8080 `
  -e GOOGLE_API_KEY=your-key `
  adaptive-chef:local
```

### Test

```powershell
curl http://localhost:8080/chat `
  -H "Content-Type: application/json" `
  -d '{\"message\": \"Create a meal plan\"}'
```

---

## Monitoring & Logs

### View Logs

```powershell
# Cloud Run logs
gcloud run services logs read adaptive-chef --region us-central1

# Cloud Functions logs
gcloud functions logs read adaptive-chef --region us-central1
```

### Monitor Performance

```powershell
# Open Cloud Console
gcloud console
# Navigate to: Cloud Run > adaptive-chef > Metrics
```

---

## Cost Estimation

### Agent Engine Pricing
- **Model**: Gemini 2.0 Flash
  - Input: $0.075 per 1M tokens
  - Output: $0.30 per 1M tokens
- **Cloud Functions**: Pay-per-invocation
  - First 2M invocations/month: FREE
  - Additional: $0.40 per 1M

### Cloud Run Pricing
- **CPU**: $0.00002400 per vCPU-second
- **Memory**: $0.00000250 per GiB-second
- **Requests**: First 2M free

**Estimated Monthly Cost (moderate use):**
- ~1000 meal plans/month: $5-10
- ~10,000 meal plans/month: $30-50

---

## Troubleshooting

### Error: "API Key Not Found"

```powershell
# Verify secret exists
gcloud secrets list

# Check IAM permissions
gcloud secrets get-iam-policy google_api_key
```

### Error: "Module not found"

```powershell
# Verify requirements.txt is complete
pip install -r requirements.txt

# Rebuild container
gcloud builds submit --tag gcr.io/YOUR_PROJECT/adaptive-chef
```

### Error: "Timeout"

```powershell
# Increase timeout for Cloud Run
gcloud run services update adaptive-chef `
  --timeout=600 `
  --region=us-central1
```

---

## Production Best Practices

1. **API Key Management**
   - Use Secret Manager (never hardcode)
   - Rotate keys regularly
   - Monitor usage

2. **Scaling**
   - Set min instances: 1 for warmer starts
   - Max instances: 10-100 based on traffic
   - Concurrency: 5-10 per instance

3. **Monitoring**
   - Enable Cloud Logging
   - Set up alerts for errors
   - Track latency metrics

4. **Security**
   - Enable authentication for production
   - Use HTTPS only
   - Implement rate limiting

---

## Deployment Evidence for Capstone (+5 pts)

Include in your submission:

1. **Screenshot** of deployed service in Cloud Console
2. **Deployment logs** showing successful deployment
3. **Test results** from production endpoint
4. **Endpoint URL** (can be provided privately to judges)

Example evidence:

```
✅ DEPLOYMENT SUCCESSFUL

Service: adaptive-chef
Region: us-central1
URL: https://adaptive-chef-abc123-uc.a.run.app
Status: READY
Last Deploy: 2025-11-15 10:30:00 UTC

Test Result:
$ curl https://adaptive-chef-abc123-uc.a.run.app/health
{"status": "healthy"}
```

---

## Cleanup (After Competition)

```powershell
# Delete Cloud Run service
gcloud run services delete adaptive-chef --region us-central1

# Delete container image
gcloud container images delete gcr.io/YOUR_PROJECT/adaptive-chef

# Delete secret
gcloud secrets delete google_api_key
```

---

For questions, see [Google Cloud Documentation](https://cloud.google.com/docs) or [ADK Docs](https://github.com/google/adk-python).
