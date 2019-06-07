"""Modelo da aplicação questionários."""

from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel


class Questionario(TimeStampedModel):
    """Questionário."""

    usuarios = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='questionarios',
        through='UsuariosQuestionarios',
        blank=True,
    )
    respostas = models.ManyToManyField(
        'Questao',
        related_name='questionarios',
        through='QuestionariosQuestoes',
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


class UsuariosQuestionarios(TimeStampedModel):
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
    AVALIACAO = 4

    tipo_questao_choices = [
        (TEXTO_LIVRE, 'Texto Livre'),
        (UNICA_ESCOLHA, 'Única Escolha'),
        (MULTIPLA_ESCOLHA, 'Múltipla Escolha'),
        (AVALIACAO, 'Avaliação'),
    ]

    questionario = models.ForeignKey(Questionario, related_name='questoes', on_delete=models.CASCADE)

    codigo = models.CharField(max_length=100)
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    requerida = models.BooleanField(default=True)
    tipo_questao = models.IntegerField(choices=tipo_questao_choices)

    class Meta:
        """todo."""

        ordering = ['id']

    def __str__(self):
        """toString."""
        return self.titulo


class QuestionariosQuestoes(TimeStampedModel):
    """Relaciona um questionário com as respostas de usuários."""

    questionario = models.ForeignKey(
        Questionario,
        related_name='questionarios_questoes',
        on_delete=models.CASCADE,
    )
    questao = models.ForeignKey(Questao, related_name='questionarios_questoes', on_delete=models.CASCADE)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='questionarios_questoes',
        on_delete=models.CASCADE,
    )

    # campos relacionados com a escolha do usuário
    resposta = models.TextField(blank=True)
    alternativa_selecionada = models.ForeignKey(
        'AlternativaQuestao',
        related_name='questionarios_questoes_alternativa_selecionada',
        on_delete=models.CASCADE,
        null=True,
    )
    alternativas_selecionadas = models.ManyToManyField(
        'AlternativaQuestao',
        related_name='questionarios_questoes_alternativas_selecionadas',
        blank=True,
    )
    item_questao = models.ForeignKey(
        'ItemQuestao',
        related_name='questionarios_questoes_item_questao',
        on_delete=models.CASCADE,
        null=True,
    )
    alternativa_item_questao = models.ForeignKey(
        'AlternativaItemQuestao',
        related_name='questionarios_questoes_alternativa_item_questao',
        on_delete=models.CASCADE,
        null=True,
    )

    def alternativas_selecionadas_texto(self):
        """Retorna uma representação textual das alternativas selecionadas."""
        return ', '.join(map(str, self.alternativas_selecionadas.all()))

    def alternativas_item_selecionados_texto(self):
        """Retorna uma representação textal dos items."""
        return f'[Item: {self.item_questao.titulo}][Alternativa: {self.alternativa_item_questao.titulo}]'

    def __str__(self):
        """toString."""
        resposta = f'Resposta do usuário "{self.usuario.username}" referente a questão '
        resposta += f'"{self.questao.titulo}" do questionário "{self.questionario.titulo}": '
        if self.questao.tipo_questao == Questao.TEXTO_LIVRE:
            resposta += f'{self.resposta}'

        elif self.questao.tipo_questao == Questao.UNICA_ESCOLHA:
            resposta += f'Alternativa: {self.alternativa_selecionada.titulo}'

        elif self.questao.tipo_questao == Questao.MULTIPLA_ESCOLHA:
            resposta += f'Alternativas: {self.alternativas_selecionadas_texto()}'

        elif self.questao.tipo_questao == Questao.AVALIACAO:
            resposta += self.alternativas_item_selecionados_texto()

        return resposta


class AlternativaQuestao(TimeStampedModel):
    """Alternativa questão."""

    UNICA_ESCOLHA = 1
    TEXTO_LIVRE = 2

    tipo_alternativa_choices = [
        (UNICA_ESCOLHA, 'Única Escolha'),
        (TEXTO_LIVRE, 'Texto'),
    ]

    questao = models.ForeignKey(Questao, related_name='alternativas', on_delete=models.CASCADE, null=True)

    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    tipo_alternativa = models.IntegerField(choices=tipo_alternativa_choices, default=UNICA_ESCOLHA)

    resposta = models.TextField(blank=True)

    class Meta:
        """todo."""

        ordering = ['id']

    def __str__(self):
        """toString."""
        return self.titulo


class ItemQuestao(TimeStampedModel):
    """Item para questões do tipo avaliação."""

    questao = models.ForeignKey(Questao, related_name='items_questao', on_delete=models.CASCADE)

    titulo = models.TextField()

    def __str__(self):
        """toString."""
        return f'Item referente a questão {self.questao.titulo}'


class AlternativaItemQuestao(TimeStampedModel):
    """Uma alternativa para item que questão do tipo avaliação."""

    UNICA_ESCOLHA = 1

    tipo_alternativa_item_questao_choices = [
        (UNICA_ESCOLHA, 'Única Escolha'),
    ]

    item_questao = models.ForeignKey(ItemQuestao, related_name='alternativas', on_delete=models.CASCADE)

    titulo = models.CharField(max_length=100)
    tipo_alternativa = models.IntegerField(
        choices=tipo_alternativa_item_questao_choices,
        default=UNICA_ESCOLHA,
    )

    def __str__(self):
        """toString."""
        return self.titulo
