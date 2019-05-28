"""Configurações de pré-produção."""

from .base import *  # noqa: F403

# Security
DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG   # noqa: F405

# cache
# MIDDLEWARE_CLASSES = (
#     ('django.middleware.cache.UpdateCacheMiddleware',)
#     + MIDDLEWARE_CLASSES
#     + ('django.middleware.cache.FetchFromCacheMiddleware',)
# )

# amazon s3
# AWS_STORAGE_BUCKET_NAME = 'igbrch-static'
# AWS_ACCESS_KEY_ID = get_environment_variable('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = get_environment_variable('AWS_SECRET_ACCESS_KEY')
# STATICFILES_LOCATION = 'static'
# STATICFILES_STORAGE = 'core.storages.StaticLocationStorage'
# MEDIAFILES_LOCATION = 'media'
# DEFAULT_FILE_STORAGE = 'core.storages.MediaLocationStorage'
