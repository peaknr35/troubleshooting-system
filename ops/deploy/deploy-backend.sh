#!/usr/bin/env bash
# Idempotent Cloud Run deploy for the backend. Safe to run repeatedly.
# Usage: PROJECT_ID=my-proj FRONTEND_ORIGIN=https://app.example.com ./deploy-backend.sh
set -euo pipefail

PROJECT_ID="${PROJECT_ID:?set PROJECT_ID}"
REGION="${REGION:-us-central1}"
SERVICE="${SERVICE:-deep-research-backend}"
FRONTEND_ORIGIN="${FRONTEND_ORIGIN:-*}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(cd "$SCRIPT_DIR/../../backend" && pwd)"

echo "Deploying $SERVICE to project $PROJECT_ID ($REGION) from $BACKEND_DIR"
gcloud config set project "$PROJECT_ID"
gcloud services enable run.googleapis.com cloudbuild.googleapis.com

gcloud run deploy "$SERVICE" \
  --source "$BACKEND_DIR" \
  --region "$REGION" \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --timeout 3600 \
  --concurrency 20 \
  --max-instances 5 \
  --set-env-vars "APP_CORS_ORIGINS=${FRONTEND_ORIGIN}"

URL="$(gcloud run services describe "$SERVICE" --region "$REGION" --format='value(status.url)')"
echo "Deployed: $URL"
echo "Health:   $URL/health"
