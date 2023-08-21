# news_server_py
News server written via django and django rest-framework

# Environment file
In  env_template you find database parameters and token parameters

Rename `env_template` to '.env' and change parameters. if you change the parameters in `.env` make sure that the `Dockerfile` and `docker-compose.yml` files are also changed

##

    POSTGRES_HOST=news_server_database - database host 
    POSTGRES_PORT=5432 - database port
    POSTGRES_USER=server - database user
    POSTGRES_PASSWORD=123 - database password
    POSTGRES_DB=database - database name
    TOKEN_LIFETIME=86400 - token life time in milliseconds
    SALT=123 - salt for password hashing

# Running

You can use docker for running server.

    docker compose up

# Endpoints
After running go the `http://localhost:8000/swagger/` to see endpoints and descriptions.

# Testing
If you use `Visual Studio Code`, you can install [rest-client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for testing endpoints.

# Project structure

    news_server_py/

    ├── docker-compose.yml
    ├── Dockerfile
    ├── env_template
    ├── fixtures
    │   └── admin.json
    ├── generate_hash.py
    ├── manage.py
    ├── news
    │   ├── admin.py
    │   ├── apps.py
    │   ├── common.py
    │   ├── exceptions.py
    │   ├── __init__.py
    │   ├── migrations
    │   │   ├── 0001_initial.py
    │   │   └── __init__.py
    │   ├── models.py
    │   ├── serializers.py
    │   ├── shared.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views
    │       ├── authors.py
    │       ├── categories.py
    │       ├── commentaries.py
    │       ├── drafts.py
    │       ├── images.py
    │       ├── news.py
    │       ├── tags.py
    │       └── users.py
    ├── news_server_py
    │   ├── asgi.py
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── README.md
    ├── requirements.txt
    └── rest-client
        ├── authors.http
        ├── categories.http
        ├── commentary.http
        ├── drafts.http
        ├── images.http
        ├── news.http
        ├── tags.http
        └── users.http



