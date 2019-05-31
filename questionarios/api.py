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
            models.UsuarioQuestionario.objects.create(
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

        questionario = shortcuts.get_object_or_404(models.Questionario, id=request.data['id'])
        models.UsuarioQuestionario.objects.filter(
            usuario=request.user,
            questionario=questionario
        ).update(submetido=True)

        return response.Response(self.get_serializer(respostas, many=True).data)


class UsuarioQuestionarioSerializer(serializers.ModelSerializer):
    """todo."""

    class Meta:
        """todo."""

        model = models.UsuarioQuestionario
        fields = '__all__'


class UsuarioQuestionarioViewSet(viewsets.ModelViewSet):
    """todo."""

    queryset = models.UsuarioQuestionario.objects.all()
    serializer_class = UsuarioQuestionarioSerializer
