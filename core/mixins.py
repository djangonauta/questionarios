"""Mixins da aplicação core."""


class SelectSerializerFieldsMixin:
    """Permite redefinir campos de exibição de um serializador."""

    param_field_names = 'field_names'

    def to_representation(self, data):
        """Seleciona os campos de exibição em função de parâmetros da solicitação."""
        data = super(SelectSerializerFieldsMixin, self).to_representation(data)
        fields = self.context['request'].query_params.get(self.param_field_names, None)
        if fields:
            fields = set(fields.split(','))
            data = {k: v for k, v in data.items() if k in fields}

        return data
