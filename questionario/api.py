"""Rotas da API."""

from rest_framework import routers

from core.api import UserViewSet
from questionarios.api import QuestionarioViewSet, RespostaQuestaoViewSet, UsuarioQuestionarioViewSet

router = routers.DefaultRouter()
router.register('usuarios', UserViewSet)
router.register('questionarios', QuestionarioViewSet)
router.register('respostas', RespostaQuestaoViewSet)
router.register('usuarios-questionarios', UsuarioQuestionarioViewSet)

urls = router.urls, 'questionario', 'v1'
