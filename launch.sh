#Launch the application using gunicorn backend
gunicorn -w 4 -b 0.0.0.0:${APP_ENDPOINT_PORT:-8045} app.main:app