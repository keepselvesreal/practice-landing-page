#!/bin/bash
# Script to inject environment variables into frontend HTML for local development

# Load environment variables from .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "Error: .env file not found"
    exit 1
fi

# Inject environment variables into index.html
sed -e "s|__GOOGLE_PLACES_API_KEY__|${GOOGLE_PLACES_API_KEY}|g" \
    -e "s|__PAYPAL_CLIENT_ID__|${PAYPAL_CLIENT_ID}|g" \
    frontend/index.html > frontend/index.html.tmp && \
    mv frontend/index.html.tmp frontend/index.html

echo "✓ Environment variables injected into frontend/index.html"
echo "  - GOOGLE_PLACES_API_KEY: ${GOOGLE_PLACES_API_KEY:0:20}..."
echo "  - PAYPAL_CLIENT_ID: ${PAYPAL_CLIENT_ID:0:20}..."
