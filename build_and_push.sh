#!/usr/bin/env bash

# build_and_push.sh — Build a Docker image (linux/amd64) and push it to Artifact Registry.
#
# Usage:
#   ./build_and_push.sh <service-name> [path]
#
# Examples:
#   ./build_and_push.sh frontend                # builds ./frontend and tags …/frontend:latest
#   ./build_and_push.sh user-service services/user-service  # builds ./services/user-service and tags …/user-service:latest
#
# Requirements:
#   * Docker buildx installed & configured (docker buildx ls)
#   * Authenticated to the target registry (gcloud auth configure-docker ...)
#
# Notes:
#   • PLATFORM is hard-coded to linux/amd64 so the images run on GKE nodes.
#   • REGISTRY points to europe-central2-docker.pkg.dev/ersms-25l-462511/ersms-app-test.

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <service-name> [path]" >&2
  exit 1
fi

SERVICE="$1"
DIR="${2:-$SERVICE}"

# Absolute path resolution for docker build context
if [[ ! -d "$DIR" ]]; then
  echo "Directory '$DIR' not found" >&2
  exit 1
fi

REGISTRY="europe-central2-docker.pkg.dev/ersms-25l-462511/ersms-app-test"
IMAGE="$REGISTRY/$SERVICE:latest"

echo "▶ Building and pushing $IMAGE from $DIR"

docker buildx build \
  --platform linux/amd64 \
  -t "$IMAGE" \
  --push \
  "$DIR"

echo "\n✔ Done: $IMAGE pushed" 