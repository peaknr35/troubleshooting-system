# Deploy the backend to Google Cloud Run

The backend is stateless and listens on `$PORT` (Cloud Run sets this). Long
research runs want a generous timeout and modest concurrency.

## One-time
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud services enable run.googleapis.com cloudbuild.googleapis.com
```

## Deploy (source-based build)
```bash
cd backend
gcloud run deploy deep-research-backend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --timeout 3600 \
  --concurrency 20 \
  --max-instances 5 \
  --set-env-vars APP_CORS_ORIGINS=https://YOUR_FRONTEND_ORIGIN
```
Notes:
- `--timeout 3600` (max) covers long multi-step research runs.
- Set `APP_CORS_ORIGINS` to your deployed frontend origin (comma-separated for
  several). Do **not** leave it as `*` once the frontend origin is known.
- No provider keys are set here — they come from each client request.

## Verify
```bash
SERVICE_URL=$(gcloud run services describe deep-research-backend --region us-central1 --format='value(status.url)')
curl "$SERVICE_URL/health"
```

## Frontend
Point the frontend at the service URL via `NEXT_PUBLIC_BACKEND_URL=$SERVICE_URL`
(rebuild the frontend — the value is inlined at build time), then deploy the
frontend to Vercel, Cloud Run, or any Node host.
