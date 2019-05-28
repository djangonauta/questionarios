"""Módulo contém views genéricas ou globais ao projeto."""

from django.contrib.auth import mixins
from django.views import generic


class IndexView(mixins.LoginRequiredMixin, generic.TemplateView):
    """Index."""

    template_name = 'base.html'


index = IndexView.as_view()
