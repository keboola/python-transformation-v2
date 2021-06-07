#!/bin/bash
set -e

echo "FROM $BASE_IMAGE" | cat - ./Dockerfile.template > ./build/Dockerfile
