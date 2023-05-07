# Sportfy

Sportfy backend, an application that connects coaches with athletes and allows for managing a sports club.

![](https://img.shields.io/badge/python-v3.11.3-blue)
![](https://img.shields.io/badge/django-v4.1.4-blue)
![](https://img.shields.io/badge/fastapi-v0.88.0-blue)
![](https://img.shields.io/badge/djangorestframework-v3.14.0-blue)
![](https://img.shields.io/badge/celery-v5.2.7-blue)
![](https://img.shields.io/badge/postgres-v15.2-blue)
![](https://img.shields.io/badge/pymongo-v4.3.3-blue)
![](https://img.shields.io/badge/redis-v7.0.11-blue)


## Required software:
- Docker and Docker compose


## Run

to run the project:
```bash
docker-compose -f local.yml build
docker-compose -f local.yml up
```

to create a superuser:
```bash
docker-compose -f local.yml run --rm django python manage.py createsuperuser
```

to run the tests:
- All tests
  ```bash
  docker-compose -f local.yml run --rm django /bin/bash
  pytest
  ```

- Specific test
  ```bash
  docker-compose -f local.yml run --rm django /bin/bash
  pytest -k <test class name>
  ```