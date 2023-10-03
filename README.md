# news_server_py
News server written via django and django rest-framework

# Environment file
In  env_template you find database parameters and token parameters

Rename `env_template` to '.env' and change parameters. If you change ports in `.env` make sure that the `Dockerfile` and `docker-compose.yml` files are also changed.

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

When the server is first started, it is loaded with administrator information. The `fixtures.json` file contains all parameters. If you want to change the admin, go to admin panel at http://localhost:8000/admin/. The default name and password is `admin`. 


# Endpoints
After running go the http://localhost:8000/swagger/ to see endpoints and descriptions.

# Testing
If you use `Visual Studio Code`, you can install [rest-client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for testing endpoints.
Or you can use curls from curls folder.

# Project structure

    news_server_py/

    ├── curls - folder with curls scripts for testing api
    │   ├── authors
    │   │   ├── delete.sh
    │   │   ├── get.sh
    │   │   ├── post.sh
    │   │   └── put.sh
    │   ├── categories
    │   │   ├── delete.sh
    │   │   ├── get.sh
    │   │   ├── post.sh
    │   │   └── put.sh
    │   ├── comments
    │   │   ├── delete.sh
    │   │   ├── get.sh
    │   │   └── post.sh
    │   ├── drafts
    │   │   ├── delete.sh
    │   │   ├── get_list.sh
    │   │   ├── get.sh
    │   │   ├── post.sh
    │   │   └── put.sh
    │   ├── images.sh
    │   ├── news
    │   │   ├── delete.sh
    │   │   ├── get_list.sh
    │   │   ├── get.sh
    │   │   └── post.sh
    │   ├── tags
    │   │   ├── delete.sh
    │   │   ├── get.sh
    │   │   ├── post.sh
    │   │   └── put.sh
    │   └── users
    │       ├── delete.sh
    │       ├── get.sh
    │       ├── login.sh
    │       ├── post.sh
    │       └── profile.sh
    ├── docker-compose.yml - docker files
    ├── Dockerfile
    ├── env_template - example of .env file
    ├── fixtures - fixtures applying in migrations
    │   └── admin.json 
    ├── generate_hash.py - small script for generating password hash
    ├── manage.py
    ├── news - main app
    │   ├── admin.py
    │   ├── apps.py
    │   ├── common.py - file with common functions 
    │   ├── exceptions.py - file with exceptions
    │   ├── __init__.py
    │   ├── migrations
    │   │   ├── 0001_initial.py
    │   │   ├── __init__.py
    │   ├── models.py
    │   ├── serializers.py - module with serializers
    │   ├── swagger.py - module with functions for generating swagger documentation
    │   ├── tests.py
    │   ├── urls.py 
    │   └── views - folder contains modules with views
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
    ├── requirements.txt - file contains a list of required libraries
    └── rest-client - folder with http requests for rest-client
        ├── authors.http
        ├── categories.http
        ├── commentary.http
        ├── drafts.http
        ├── images.http
        ├── news.http
        ├── tags.http
        └── users.http


# TO DO
 write test (maybe)