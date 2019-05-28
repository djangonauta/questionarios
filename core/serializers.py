"""Serializadores da aplicação core."""

from django.contrib import auth
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""

    class Meta:
        model = auth.get_user_model()
        fields = ['id', 'username']


class DisableSignupSerializer(serializers.Serializer):
    """Serializador customizado."""

    def validate(self, data):
        """Desativa a criação de novas contas."""
        raise serializers.ValidationError('Registro de novas contas temporariamente suspenso.')
