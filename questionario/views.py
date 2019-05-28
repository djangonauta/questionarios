"""Módulo contém views genéricas ou globais ao projeto."""

from django.views import generic


class IndexView(generic.TemplateView):
    """Index."""

    template_name = 'base.html'


index = IndexView.as_view()
