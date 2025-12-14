#!/usr/bin/env bash
# Start script for Render.com

set -o errexit  # Exit on error

echo "Starting Gunicorn..."
exec gunicorn core.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers ${WORKERS:-2} \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -




