"""Automaticamente carrega funcionalidades quando a aplicação inicia."""

from .celery import app as celery_app

__all__ = ('celery_app',)