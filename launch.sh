#Launch the application using gunicorn backend
gunicorn -w 4 -b 0.0.0.0:5000 app.main:app