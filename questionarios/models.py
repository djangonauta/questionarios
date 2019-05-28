"""Modelo da aplicação questionários."""

from django.db import models
from model_utils.models import TimeStampedModel


class Questionario(TimeStampedModel):
    """Questionário."""

    titulo = models.CharField(max_length=255)
    descricao = models.TextField()

    def __str__(self):
        """toString."""
        return self.titulo


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

    tipo_questao = models.IntegerField(choices=tipoChoices)
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    resposta = models.TextField()

    def __str__(self):
        """toString."""
        return self.titulo


class AlternativaQuestao(TimeStampedModel):
    """Alternativa questão."""

    questao = models.ForeignKey(Questao, related_name='alternativas', on_delete=models.CASCADE)

    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    resposta = models.TextField()
    selecionada = models.BooleanField()

    def __str__(self):
        """toString."""
        return self.titulo
