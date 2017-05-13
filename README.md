django-forum
============

<p align="center">
    <img src="docs/screenshot.png">
</p>

Description
-----------

This forum is mainly an example of how [Docker Compose](https://docs.docker.com/compose/overview/) may be used
in development (instead of [virtualenv](https://virtualenv.pypa.io/en/stable/)) and deployment of a Django website.

The website contains several components: a MySQL server, a Django back-end, and nginx (which is placed in front of them
in production mode).
Thanks to Compose, you don't need to install, configure, or start these components yourself (either in development or
production).
All configuration is stored in this repository, so Compose can pull and run all these servers
in isolated containers for you.

Furthermore, it's easy to plug in new components (e.g. Celery for background processing or
Elasticsearch for full-text search).
Once you wrote and pushed proper configuration files, it's enough for other developers in your team
to pull the repository and restart Compose.

Besides, isolation of processes in containers gives additional scalability and security.

Setting up a development environment
------------------------------------

*This instruction is only applicable for Linux.*

1. Install [Docker Compose](https://docs.docker.com/compose/install/).

2. Clone this repository:

    ```bash
    git clone https://github.com/borzunov/forum.git && cd forum
    ```

3. Start containers:

        docker-compose up --build

4. Wait a minute, while containers are downloading, MySQL is setting up,
   and Django migrations are applied to the newly created database.

    The development server will start at [http://localhost:8000/](http://localhost:8000/).
    It will watch for changes in `web` directory and (usually) load a new version of code automatically.

5. To create a superuser or make migrations for a Django app, you can call `manage.py` in the following way:

        docker-compose run --rm web manage.py createsuperuser
        docker-compose run --rm web manage.py makemigrations forum

Setting up a production environment
-----------------------------------

*This instruction is only applicable for Linux.*

1. Install [Docker Compose](https://docs.docker.com/compose/install/).

2. Clone this repository to `/var/www/forum`:

    ```bash
    git clone https://github.com/borzunov/forum.git /var/www/forum && cd /var/www/forum
    ```

3. Copy `development.env` to `production.env` and specify production settings:

    - Change `ENVIRONMENT` to `production`

    - Specify a website `HOST`

    - Generate `DJANGO_SECRET_KEY` using a secure random generator:

        ```bash
        cat /dev/urandom | tr -dc '[[:print:]]' | head -c 50 && echo
        ```

    - Specify reliable database passwords

    - [Sign up](https://www.google.com/recaptcha/intro/index.html) for reCAPTCHA and specify your keys

    - Register a email for sending activation links and specify the SMTP credentials

    Make a backup of `production.env` on the server because it is not stored in the repository.
    But do not add it to the repository because it contains confidential information
    about your production environment!

4. Register a systemd unit to run Compose on server startup and log its output:

        sudo cp deploy/systemd/forum.service /etc/systemd/system
        sudo systemctl enable forum

    Then start Compose:

        sudo systemctl start forum

    This will start [gunicorn](http://gunicorn.org/) behind nginx to serve the Django website in production mode.
    Now your website is ready.

    You can watch Compose output (and find the reason of problems, if any) using:

        sudo journalctl -u forum -o cat -f

5. When the repository is updated, run:

        git pull
        sudo systemctl restart forum
