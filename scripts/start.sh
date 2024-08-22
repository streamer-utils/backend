cd /app

alembic --config ./app/alembic.ini upgrade head

exec uvicorn --reload --host 0.0.0.0 --port 80 main:app
