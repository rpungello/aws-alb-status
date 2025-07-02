#!/usr/bin/env bash

set -e

# Make sure we have the required commands to run this script
if ! command -v semver &>/dev/null; then
    echo "semver is required to run this script"
    exit 1
fi

# Read the current version from composer.json
CURRENT_VERSION=$(<VERSION)

# Read the increment argument (if provided)
INCREMENT=$1

# If $INCREMENT is not empty, run semver to increment the version, then update composer.json and create a git tag
if [ -n "$INCREMENT" ]; then
    # Increment composer version
    VERSION=$(semver --increment "$INCREMENT" "$CURRENT_VERSION")
    echo $VERSION >VERSION

    git add VERSION
    git commit -qm "Bump version to $VERSION"
    git tag -a -m "Tagging version $VERSION" "$VERSION"
else
    VERSION=$CURRENT_VERSION
fi

# Extract semver components
IFS='.' read -r MAJOR MINOR PATCH <<< "$VERSION"

# Build the Docker image
echo "Building AWS ALB Status Check v$VERSION"
docker buildx build \
       --pull \
       --no-cache \
       --build-arg VERSION="$VERSION" \
       --platform=linux/amd64,linux/arm64/v8 \
       --tag "692057070962.dkr.ecr.us-east-1.amazonaws.com/aws-alb-status:${MAJOR}.${MINOR}.${PATCH}" \
       --tag "692057070962.dkr.ecr.us-east-1.amazonaws.com/aws-alb-status:${MAJOR}.${MINOR}" \
       --tag "692057070962.dkr.ecr.us-east-1.amazonaws.com/aws-alb-status:${MAJOR}" \
       --tag "692057070962.dkr.ecr.us-east-1.amazonaws.com/aws-alb-status:latest" \
       --push .
