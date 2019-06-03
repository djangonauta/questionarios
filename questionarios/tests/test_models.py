"""Model Tests."""


import datetime

from django import test
from django.contrib.auth import get_user_model

from .. import models

User = get_user_model()


class QuestionarioTest(test.TestCase):
    """Questionários teste."""

    @classmethod
    def setUpTestData(cls):
        """Class fixtures."""
        usuarios = []
        for i in range(5):
            user = User.objects.create_user(username=f'usuario{i}', password=f'pass{i}')
            usuarios.append(user)

        cls.usuarios = usuarios
        return super(QuestionarioTest, cls).setUpTestData()

    def test_questionario(self):
        """todo."""
        questionario = models.Questionario.objects.create(
            titulo='Questionário 1',
            descricao='',
            inicio=datetime.datetime.now(),
        )

        questao_1 = models.Questao.objects.create(
            questionario=questionario,
            titulo='Escolha uma das opções a seguir',
            tipo_questao=models.Questao.UNICA_ESCOLHA,
        )
        alternativa_sim = models.AlternativaQuestao.objects.create(
            questao=questao_1,
            titulo='sim',
        )
        alternativa_nao = models.AlternativaQuestao.objects.create(  # noqa
            questao=questao_1,
            titulo='não',
        )

        questao_2 = models.Questao.objects.create(
            questionario=questionario,
            titulo='Escolha quantas opções forem necessárias',
            tipo_questao=models.Questao.MULTIPLA_ESCOLHA,
        )
        alternativa_a = models.AlternativaQuestao.objects.create(
            questao=questao_2,
            titulo='A'
        )
        alternativa_b = models.AlternativaQuestao.objects.create(
            questao=questao_2,
            titulo='B'
        )
        alternativa_c = models.AlternativaQuestao.objects.create(  # noqa
            questao=questao_2,
            titulo='C'
        )
        alternativa_d = models.AlternativaQuestao.objects.create(
            questao=questao_2,
            titulo='D'
        )
        alternativa_e = models.AlternativaQuestao.objects.create(  # noqa
            questao=questao_2,
            titulo='E'
        )

        questao_3 = models.Questao.objects.create(  # noqa
            questionario=questionario,
            titulo='Responda a questão a seguir',
            tipo_questao=models.Questao.TEXTO_LIVRE,
        )

        resposta_questao_1 = models.QuestionariosQuestoes.objects.create(  # noqa
            questionario=questionario,
            usuario=self.usuarios[0],
            questao=questao_1,
            alternativa_selecionada=alternativa_sim,
        )

        resposta_questao_2 = models.QuestionariosQuestoes.objects.create(
            questionario=questionario,
            usuario=self.usuarios[0],
            questao=questao_2,
        )
        resposta_questao_2.alternativas_selecionadas.set([
            alternativa_a,
            alternativa_b,
            alternativa_d
        ])

        resposta_questao_3 = models.QuestionariosQuestoes.objects.create(  # noqa
            questionario=questionario,
            usuario=self.usuarios[0],
            questao=questao_3,
            resposta='Resposta da questão 3',
        )

        models.UsuariosQuestionarios.objects.create(
            questionario=questionario,
            usuario=self.usuarios[0],
            submetido=True,
        )
        respostas = models.QuestionariosQuestoes.objects.filter(
            questionario=questionario,
            usuario=self.usuarios[0],
        )
        for resposta in respostas:
            print(resposta, end='\n\n')
