FROM python:3.11.3

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  postgresql-client\
  # Translations dependencies
  gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/* 

# Requirements are installed here to ensure they will be cached.
RUN python -m pip install --upgrade pip

COPY ./web-2/requirements /requirements

RUN pip install -r /requirements/local.txt

COPY ./compose/local/fastapi/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

WORKDIR /web-2