"""Api da aplicação core."""

from django.contrib import auth
from rest_framework import permissions, viewsets

from . import serializers


class UserViewSet(viewsets.ModelViewSet):
    """User viewset."""

    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAdminUser,)
    queryset = auth.get_user_model().objects.all()
