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
            titulo='Questionario 1',
            descricao='descricao questionario 1',
            inicio=datetime.datetime(2019, 10, 10)
        )

        q1 = models.Questao.objects.create(
            titulo='Primeira questão',
            tipo_questao=models.Questao.MULTIPLA_ESCOLHA,
            questionario=questionario,
        )

        a = models.AlternativaQuestao.objects.create(
            titulo='A',
            questao=q1
        )

        b = models.AlternativaQuestao.objects.create(
            titulo='B',
            questao=q1
        )

        c = models.AlternativaQuestao.objects.create(
            titulo='C',
            questao=q1
        )

        self.assertEqual(models.Questionario.objects.count(), 1)
        self.assertEqual(models.Questao.objects.count(), 1)
        self.assertEqual(models.AlternativaQuestao.objects.count(), 3)

        models.RespostaQuestao.objects.create(
            questao=q1,
            alternativa=b,
            usuario=self.usuarios[0]
        )

        models.RespostaQuestao.objects.create(
            questao=q1,
            alternativa=a,
            usuario=self.usuarios[1]
        )

        models.RespostaQuestao.objects.create(
            questao=q1,
            alternativa=c,
            usuario=self.usuarios[2]
        )

        models.RespostaQuestao.objects.create(
            questao=q1,
            alternativa=c,
            usuario=self.usuarios[3]
        )

        models.RespostaQuestao.objects.create(
            questao=q1,
            alternativa=a,
            usuario=self.usuarios[4]
        )

        self.assertEqual(
            models.RespostaQuestao.objects.filter(usuario=self.usuarios[3], questao=q1)[0].alternativa.titulo,
            'C'
        )
