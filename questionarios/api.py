"""Questionarios api."""

from rest_framework import decorators, permissions, response, serializers, viewsets

from core.pagination import CorePaginator

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
    respostas = serializers.ReadOnlyField()

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


class RespostaQuestaoSerializer(serializers.ModelSerializer):
    """Resposta questionário."""

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
        import pprint
        for questao in request.data.pop('questoes'):
            questao['questao'] = request.data['id']
            questao['usuario'] = request.user.id
            serializer = self.get_serializer(data=questao)
            if serializer.is_valid():
                models.RespostaQuestao.objects.create(**serializer.validated_data)
            else:
                pprint.pprint(serializer.errors)

        return response.Response()
