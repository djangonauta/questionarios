"""Rotas da API."""

from rest_framework import routers

from core.api import UserViewSet
from questionarios.api import QuestionariosQuestoesViewSet, QuestionarioViewSet, UsuariosQuestionariosViewSet

router = routers.DefaultRouter()
router.register('usuarios', UserViewSet)
router.register('questionarios', QuestionarioViewSet)
router.register('questionarios-questoes', QuestionariosQuestoesViewSet)
router.register('usuarios-questionarios', UsuariosQuestionariosViewSet)

urls = router.urls, 'questionario', 'v1'
