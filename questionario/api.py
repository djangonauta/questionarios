"""Rotas da API."""

from rest_framework import routers

from core.api import UserViewSet

router = routers.DefaultRouter()
router.register('usuarios', UserViewSet)

urls = router.urls, 'questionario', 'v1'
