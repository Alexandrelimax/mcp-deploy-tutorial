#!/bin/bash

PROJECT_ID="" 
ARTIFACT_ID=""
IMAGE_NAME="***-image"
CLOUD_RUN_SERVICE_NAME="mcp-***"
VERSION="v1"
REGION="us-central1"
IMAGE="$REGION-docker.pkg.dev/$PROJECT_ID/$ARTIFACT_ID/$IMAGE_NAME:$VERSION"


echo "🔐 Autenticando no Artifact Registry..."
gcloud config set project $PROJECT_ID 
gcloud auth configure-docker $REGION-docker.pkg.dev
gcloud config set run/region $REGION


echo "🔨 Construindo a imagem Docker..."
docker build -t $IMAGE .


echo "📤 Enviando a imagem para o Artifact Registry..."
docker push $IMAGE


echo "☁️ Fazendo deploy para o Cloud Run..."
gcloud run deploy $CLOUD_RUN_SERVICE_NAME \
  --image $IMAGE \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8000 \


echo "✅ Deploy concluído com sucesso!"
gcloud run services describe $CLOUD_RUN_SERVICE_NAME --region $REGION --format "value(status.url)"