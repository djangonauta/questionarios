"""Questionarios api."""

from django import shortcuts
from rest_framework import decorators, permissions, response, serializers, viewsets

from core.pagination import CorePaginator
from core.serializers import UserSerializer

from . import models


class AlternativaSerializer(serializers.ModelSerializer):
    """todo."""

    class Meta:
        """todo."""

        model = models.AlternativaQuestao
        exclude = ['questao']


class QuestaoSerializer(serializers.ModelSerializer):
    """todo."""

    alternativas = AlternativaSerializer(many=True)
    tipo_questao_display = serializers.ReadOnlyField(source='get_tipo_questao_display')

    class Meta:
        """todo."""

        model = models.Questao
        exclude = ['questionario']


class QuestionarioSerializer(serializers.ModelSerializer):
    """todo."""

    questoes = QuestaoSerializer(many=True)

    class Meta:
        """todo."""

        model = models.Questionario
        fields = '__all__'

    def create(self, validated_data):
        """todo."""
        questoes_data = validated_data.pop('questoes')
        questionario = models.Questionario.objects.create(**validated_data)
        for questao_data in questoes_data:
            alternativas_data = questao_data.pop('alternativas')
            questao = models.Questao.objects.create(questionario=questionario, **questao_data)
            for alternativa_data in alternativas_data:
                models.AlternativaQuestao.objects.create(questao=questao, **alternativa_data)

        return questionario


class QuestionarioViewSet(viewsets.ModelViewSet):
    """todo."""

    queryset = models.Questionario.objects.all()
    serializer_class = QuestionarioSerializer
    pagination_class = CorePaginator


class QuestaoSerializerList(serializers.ModelSerializer):
    """todo."""

    alternativas = AlternativaSerializer(many=True)
    tipo_questao_display = serializers.ReadOnlyField(source='get_tipo_questao_display')

    class Meta:
        """Meta."""

        model = models.Questao
        exclude = ['usuarios', 'created', 'modified']


class RespostaQuestaoSerializer(serializers.ModelSerializer):
    """Resposta questionário."""

    usuario_data = UserSerializer(source='usuario', read_only=True)
    questao_data = QuestaoSerializerList(source='questao', read_only=True)

    class Meta:
        """Meta opções do serializador."""

        model = models.RespostaQuestao
        fields = '__all__'


class RespostaQuestaoViewSet(viewsets.ModelViewSet):
    """todo."""

    queryset = models.RespostaQuestao.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = RespostaQuestaoSerializer

    def perform_create(self, serializer):
        """Create."""
        serializer.save(usuario=self.request.user)

    @decorators.action(detail=False, methods=['POST'])
    def submeter(self, request, pk=None):
        """Submeter."""
        respostas = []
        for questao_dict in request.data.pop('questoes'):
            data = dict(
                questao=questao_dict.pop('id'),
                usuario=request.user.id
            )
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                data['usuario'] = request.user
                data['questao'] = shortcuts.get_object_or_404(models.Questao, id=data['questao'])

                tipo_questao = questao_dict['tipo_questao']
                if tipo_questao == models.Questao.TEXTO_LIVRE:
                    data['resposta'] = questao_dict['resposta']

                elif tipo_questao == models.Questao.UNICA_ESCOLHA:
                    data['alternativa_selecionada'] = shortcuts.get_object_or_404(
                        models.AlternativaQuestao,
                        id=questao_dict['alternativa_selecionada']
                    )

                resposta = models.RespostaQuestao.objects.create(**data)
                if tipo_questao == models.Questao.MULTIPLA_ESCOLHA:
                    resposta.alternativas_selecionadas.set(questao_dict['alternativas_selecionadas'])

                respostas.append(resposta)

            else:
                return response.Response(serializer.errors)

        return response.Response(self.get_serializer(respostas, many=True).data)
