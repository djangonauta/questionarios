"""Rotas da API."""

from rest_framework import routers

from core.api import UserViewSet
from questionarios.api import QuestionarioViewSet, RespostaQuestaoViewSet

router = routers.DefaultRouter()
router.register('usuarios', UserViewSet)
router.register('questionarios', QuestionarioViewSet)
router.register('respostas', RespostaQuestaoViewSet)

urls = router.urls, 'questionario', 'v1'
