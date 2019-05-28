"""Modelos da aplicação core."""

import hashlib

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.contrib.auth import models
from model_utils.models import TimeStampedModel


class User(TimeStampedModel, models.AbstractUser):
    """Usuário base do projeto."""

    class Meta:
        """Model meta."""

        verbose_name = 'Usuário'

    history = AuditlogHistoryField()

    def gravatar_url(self):
        """Obtém a url gravatar em função do email fornecido."""
        return '//www.gravatar.com/avatar/{}'.format(hashlib.md5(self.email.encode('utf-8')).hexdigest())


auditlog.register(User)
