#!/bin/sh

echo "🚀 Waiting for PostgreSQL to be ready..."
while ! nc -z db 5432; do
  sleep 1
done

echo "📦 Running migrations..."
python manage.py migrate --noinput

echo "🧹 Collecting static files in background..."
python manage.py collectstatic --noinput > /dev/null 2>&1 &

echo "✅ Starting server..."
exec gunicorn project.wsgi:application --bind 0.0.0.0:8000