"""Este módulo contem tags e filtros globais em relação ao projeto."""

from django import template, urls

register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, nome_url):
    """Verifica se a url atual corresponde a url nomeada para gerar a classe ativa no metismenu."""
    return 'active' if context['request'].get_full_path() == urls.reverse(nome_url) else ''
