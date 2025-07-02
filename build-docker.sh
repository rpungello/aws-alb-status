#!/usr/bin/env bash

set -e

# Read the current version from composer.json
CURRENT_VERSION=$(git describe --tags --abbrev=0)

# Build the Docker image
echo "Building AWS ALB Status Check v$VERSION"
docker buildx build \
       --pull \
       --no-cache \
       --tag "aws-alb-status:latest" \
       --load .
