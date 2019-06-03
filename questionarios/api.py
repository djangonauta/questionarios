"""Questionarios api."""

from django import shortcuts
from django.contrib import auth
from rest_framework import decorators, permissions, response, serializers, viewsets

from core.pagination import CorePaginator
from core.serializers import UserSerializer

from . import models


class SubAlternativaSerializer(serializers.ModelSerializer):
    """todo."""

    class Meta:
        """todo."""

        model = models.AlternativaQuestao
        exclude = ['questao']


class AlternativaSerializer(serializers.ModelSerializer):
    """todo."""

    alternativas = SubAlternativaSerializer(required=False, many=True)

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
        questoes_list_dict = validated_data.pop('questoes')
        questionario = models.Questionario.objects.create(**validated_data)
        for questao_dict in questoes_list_dict:
            alternativas_list_dict = questao_dict.pop('alternativas', [])
            questao = models.Questao.objects.create(questionario=questionario, **questao_dict)
            for alternativa_dict in alternativas_list_dict:
                sub_alternativa_list_dict = alternativa_dict.pop('alternativas', [])
                alternativa = models.AlternativaQuestao.objects.create(questao=questao, **alternativa_dict)
                for sub_alternativa_dict in sub_alternativa_list_dict:
                    sub_alternativa_dict.pop('alternativas', [])
                    models.AlternativaQuestao.objects.create(
                        alternativa=alternativa,
                        **sub_alternativa_dict
                    )

        for usuario in auth.get_user_model().objects.all():
            models.UsuariosQuestionarios.objects.create(
                questionario=questionario,
                usuario=usuario,
                submetido=False,
            )

        return questionario


class QuestionarioViewSet(viewsets.ModelViewSet):
    """todo."""

    queryset = models.Questionario.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = QuestionarioSerializer
    pagination_class = CorePaginator

    @decorators.action(detail=False, methods=['GET'])
    def validos(self, request, pk=None):
        """Questionários não submetidos."""
        questionarios = self.get_queryset().filter(
            usuarios_questionarios__usuario=request.user,
            usuarios_questionarios__submetido=False,
        )

        page = self.paginate_queryset(questionarios)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(questionarios, many=True)
        return response.Response(serializer.data)


class QuestaoSerializerList(serializers.ModelSerializer):
    """todo."""

    alternativas = AlternativaSerializer(many=True)
    tipo_questao_display = serializers.ReadOnlyField(source='get_tipo_questao_display')

    class Meta:
        """Meta."""

        model = models.Questao
        exclude = ['created', 'modified']


class QuestionariosQuestoesSerializer(serializers.ModelSerializer):
    """Resposta questionário."""

    usuario_data = UserSerializer(source='usuario', read_only=True)
    questao_data = QuestaoSerializerList(source='questao', read_only=True)

    class Meta:
        """Meta opções do serializador."""

        model = models.QuestionariosQuestoes
        fields = '__all__'


class QuestionariosQuestoesViewSet(viewsets.ModelViewSet):
    """todo."""

    queryset = models.QuestionariosQuestoes.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = QuestionariosQuestoesSerializer

    def perform_create(self, serializer):
        """Create."""
        serializer.save(usuario=self.request.user)

    @decorators.action(detail=False, methods=['POST'])
    def submeter(self, request, pk=None):
        """Submeter."""
        for q in request.data:
            q['usuario'] = request.user.id

        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            import pprint
            pprint.pprint(serializer.validated_data)
            for questionario_questao_dict in serializer.validated_data:
                alternativas_selecionadas = questionario_questao_dict.pop('alternativas_selecionadas', [])
                questionario = models.QuestionariosQuestoes.objects.create(**questionario_questao_dict)
                if alternativas_selecionadas:
                    questionario.alternativas_selecionadas.set(alternativas_selecionadas)

            models.UsuariosQuestionarios.objects.filter(
                usuario=request.user,
                questionario=serializer.validated_data[0]['questionario']
            ).update(submetido=True)

            return response.Response('ok')

        else:
            print(serializer.errors)
            return response.Response('erro')


class UsuariosQuestionariosSerializer(serializers.ModelSerializer):
    """todo."""

    class Meta:
        """todo."""

        model = models.UsuariosQuestionarios
        fields = '__all__'


class UsuariosQuestionariosViewSet(viewsets.ModelViewSet):
    """todo."""

    queryset = models.UsuariosQuestionarios.objects.all()
    serializer_class = UsuariosQuestionariosSerializer
