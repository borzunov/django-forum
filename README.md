forum
=====

Toy dockerized Django forum

Description
-----------

This forum is mainly an example of how [Docker Compose](https://docs.docker.com/compose/overview/) may be used
in development (instead of [virtualenv](https://virtualenv.pypa.io/en/stable/)) and deployment of a Django website.

The website contains several components: a MySQL server, a Django back-end, and nginx (which is placed in front of them
production mode).
Thanks to Compose, you don't need to install, configure, or start these components yourself (either in development or
in production).
All configuration is stored inside this repository, so Compose can pull and run all these servers
in isolated containers for you.

Furthermore, it's easy to plug in new components (e.g. Celery for background processing or
Elasticsearch for full-text search).
Once you wrote proper configuration files, it's enough for other developers in your team
to pull the repository and restart Compose.

In addition, separation processes for containers gives additional scalability and security.

![Screenshot](docs/screenshot.png)
