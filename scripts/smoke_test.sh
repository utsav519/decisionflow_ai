#!/usr/bin/env bash

set -euo pipefail

BACKEND_URL="${BACKEND_URL:-http://localhost:8000}"

echo "1. Checking health endpoint"
curl \
  --fail \
  --silent \
  --show-error \
  "${BACKEND_URL}/health"
echo

echo "2. Checking readiness endpoint"
curl \
  --fail \
  --silent \
  --show-error \
  "${BACKEND_URL}/ready"
echo

echo "3. Checking correlation-ID propagation"
headers_file="$(mktemp)"

curl \
  --fail \
  --silent \
  --show-error \
  -H "X-Correlation-ID: cor_smoke_001" \
  -D "${headers_file}" \
  -o /dev/null \
  "${BACKEND_URL}/health"

grep -i "X-Correlation-ID: cor_smoke_001" "${headers_file}"

rm -f "${headers_file}"

echo "Baseline smoke tests passed."
