
#!/bin/bash
set -e

APP_DIR="/opt/student-app"
IMAGE_NAME="student-app"
CONTAINER_NAME="student-app"

echo "Starting Student Result Predictor deployment..."

cd "$APP_DIR"

echo "Building latest Docker image..."
docker build --no-cache -t "$IMAGE_NAME" .

echo "Removing old container if present..."
docker rm -f "$CONTAINER_NAME" 2>/dev/null || true

echo "Starting updated container..."
docker run -d \
    --name "$CONTAINER_NAME" \
    --restart unless-stopped \
    -p 80:5000 \
    "$IMAGE_NAME"

echo "Waiting for application to start..."
sleep 5

echo "Checking application health..."
if ! curl -fsS http://localhost/ > /dev/null; then
    echo "ERROR: Application health check failed."
    docker logs "$CONTAINER_NAME" || true
    exit 1
fi

echo "Deployment successful!"
docker ps --filter "name=$CONTAINER_NAME"
curl -fsS http://localhost/ | grep -E "Student Result Predictor|Model Version"
