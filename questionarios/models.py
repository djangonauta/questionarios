"""Modelo da aplicação questionários."""

from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel


class Questionario(TimeStampedModel):
    """Questionário."""

    usuarios = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='questionarios',
        through='UsuarioQuestionario',
        blank=True,
    )

    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    inicio = models.DateTimeField()
    fim = models.DateTimeField(null=True)

    class Meta:
        """todo."""

        ordering = ['id']

    def __str__(self):
        """toString."""
        return self.titulo


class UsuarioQuestionario(TimeStampedModel):
    """Relaciona usuários com questionários."""

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='usuarios_questionarios',
        on_delete=models.CASCADE,
    )
    questionario = models.ForeignKey(
        Questionario,
        related_name='usuarios_questionarios',
        on_delete=models.CASCADE,
    )
    submetido = models.BooleanField()

    class Meta:
        """todo."""

        unique_together = ['usuario', 'questionario']


class Questao(TimeStampedModel):
    """Questao de um questionário."""

    TEXTO_LIVRE = 1
    UNICA_ESCOLHA = 2
    MULTIPLA_ESCOLHA = 3

    tipoChoices = [
        (TEXTO_LIVRE, 'Texto Livre'),
        (UNICA_ESCOLHA, 'Única Escolha'),
        (MULTIPLA_ESCOLHA, 'Múltipla Escolha'),
    ]

    questionario = models.ForeignKey(Questionario, related_name='questoes', on_delete=models.CASCADE)
    usuarios = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='questoes',
        through='RespostaQuestao'
    )

    tipo_questao = models.IntegerField(choices=tipoChoices)
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)

    class Meta:
        """todo."""

        ordering = ['id']

    def __str__(self):
        """toString."""
        return self.titulo


class AlternativaQuestao(TimeStampedModel):
    """Alternativa questão."""

    questao = models.ForeignKey(Questao, related_name='alternativas', on_delete=models.CASCADE)

    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    resposta = models.TextField(blank=True)

    class Meta:
        """todo."""

        ordering = ['id']

    def __str__(self):
        """toString."""
        return self.titulo


class RespostaQuestao(TimeStampedModel):
    """Resposta de uma determinada questão."""

    questao = models.ForeignKey(Questao, related_name='respostas_questao', on_delete=models.CASCADE)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='respostas_questao',
        on_delete=models.CASCADE
    )

    # campos relacionados com a escolha do usuário
    resposta = models.TextField(blank=True)
    alternativa_selecionada = models.ForeignKey(
        'AlternativaQuestao',
        related_name='resposta_questao_selecionada',
        on_delete=models.CASCADE,
        null=True
    )
    alternativas_selecionadas = models.ManyToManyField(
        'AlternativaQuestao',
        related_name='respostas_questoes_selecionadas',
        blank=True
    )

    class Meta:
        """todo."""

        unique_together = ['questao', 'usuario']
