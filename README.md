# ShildiChat

This is the backend of the kanban board widget for schildichat

# Instructions for launching

- Clone repository
- Create an .env file in the root directory and add the data from the example below
- Build containers - sudo docker-compose build
- Running containers - sudo docker-compose up

# Environment

PROJECT_NAME=shildi_chat
MAIN_DIR=apps
DB_USER={DB_USER}
DB_PASSWORD={DB_PASSWORD}
DB_NAME={DB_NAME}
DB_HOST=db
DB_PORT=5432
MEDIA_PATH={MEDIA_PATH}
STATIC_PATH={STATIC_PATH}
LOG_PATH={LOG_PATH}
MEDIA_URL=https://localhost:6777/media/
STATIC_URL=https://localhost:6777/static/
SECRET_KEY={SECRET_KEY}
DJANGO_SETTINGS_MODULE=config.settings
GUNICORN_WORKERS_COUNT=1
PYTHONUNBUFFERED=1