#!/bin/bash
set -e

case "$1" in
"manage.py")
    dockerize -wait tcp://db:3306 -timeout 1m

    exec python "$@"
    ;;
"runserver")
    dockerize -wait tcp://db:3306 -timeout 1m

    python manage.py migrate --noinput

    exec python manage.py runserver 0.0.0.0:8000
    ;;
"web")
    dockerize -wait tcp://db:3306 -timeout 1m

    python manage.py collectstatic --noinput
    python manage.py migrate --noinput

    exec gunicorn project.wsgi --config gunicorn.conf.py
    ;;
*)
    exec "$@"
    ;;
esac
