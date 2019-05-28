"""Configuração de administração da aplicação core."""

from django.contrib import admin, auth
from django.contrib.auth.admin import UserAdmin


@admin.register(auth.get_user_model())
class UserModelAdmin(UserAdmin):
    """Registra o usuário base na aplicação admin."""
