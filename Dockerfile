FROM python:3.12-slim

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

RUN pip install supervisor

COPY . /code/

RUN python manage.py migrate

RUN python manage.py collectstatic --noinput

# Create supervisor config
RUN echo "[supervisord]\n\
nodaemon=true\n\
\n\
[program:django]\n\
command=python manage.py runserver 0.0.0.0:8000\n\
directory=/code\n\
autostart=true\n\
autorestart=true\n\
\n\
[program:celery_worker]\n\
command=celery -A myproject worker --loglevel=info\n\
directory=/code\n\
autostart=true\n\
autorestart=true\n\
\n\
[program:celery_beat]\n\
command=celery -A myproject beat --loglevel=info\n\
directory=/code\n\
autostart=true\n\
autorestart=true\n\
" > /code/supervisord.conf

CMD ["supervisord", "-c", "/code/supervisord.conf"]
