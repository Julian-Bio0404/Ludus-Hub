"""Production settings."""

from .base import INSTALLED_APPS, env

DEBUG = False

# Anymail (Mailgun)
INSTALLED_APPS += ['anymail']
EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
ANYMAIL = {
    'MAILGUN_API_KEY': env('MAILGUN_API_KEY'),
    'MAILGUN_SENDER_DOMAIN': env('MAILGUN_DOMAIN')
}

# Gunicorn
INSTALLED_APPS += ['gunicorn']

# Elasticsearch
ELASTICSEARCH_DEFAULT_ALIAS_HOST = env('ELASTICSEARCH_DEFAULT_ALIAS_HOST', default='elasticsearch:9200')
ELASTIC_SEARCH_INDEX_PREFIX = ''
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': ELASTICSEARCH_DEFAULT_ALIAS_HOST,
        'http_auth': (env('ELASTIC_USER'), env('ELASTIC_PASSWORD')),
    },
}
