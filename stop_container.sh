
#!/bin/bash
set -e

echo "Stopping existing Student Result Predictor container..."

if docker ps -a --format '{{.Names}}' | grep -qx 'student-app'; then
    docker rm -f student-app
else
    echo "No existing container found. Continuing..."
fi

echo "Stop step completed."
