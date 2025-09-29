#!/bin/sh

echo "Running Database Migrations..."
uv run manage.py boom

exec "$@"