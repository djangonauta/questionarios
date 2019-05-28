"""Testa o módulo mixins da aplicação core."""

import unittest

from rest_framework import generics, serializers, test

from .. import mixins


class MySerializer(mixins.SelectSerializerFieldsMixin, serializers.Serializer):
    """Serializer fixture."""

    param_field_names = 'campos'

    name = serializers.CharField()
    age = serializers.IntegerField()
    role = serializers.CharField()
    language = serializers.CharField()

    def save(self):
        """No op."""


class MyView(generics.CreateAPIView):
    """View fixture."""

    serializer_class = MySerializer


class TestSelectSerializerFieldsMixin(unittest.TestCase):
    """Testa o mixin."""

    def test_parâmetros(self):
        """Verifica se a resposta contém apenas os campos especificados."""
        data = dict(name='igor', age=32, role='developer', language='python')
        request = test.APIRequestFactory().post('/?campos=name,role,campo_não_existente,role', data)
        response = MyView.as_view()(request)
        self.assertDictEqual(response.data, dict(name='igor', role='developer'))
