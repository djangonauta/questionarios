"""Módulo de configuração celery."""

import os

import celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questionario.settings')

app = celery.Celery('questionario')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
