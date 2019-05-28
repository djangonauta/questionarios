"""Módulo de configuração de urls do projeto."""

from django.conf import settings, urls
from django.conf.urls import static
from django.contrib import admin
from rest_framework import documentation

from . import api, views

urlpatterns = [
    urls.url(r'^$', views.index, name='index'),
    urls.url(r'^contas/', urls.include('allauth.urls')),
    urls.url(r'^api/v1/', api.urls),
    urls.url(r'^api-auth/', urls.include('rest_framework.urls', namespace='rest_framework')),
    urls.url(r'^admin/', admin.site.urls),
    urls.url(r'^docs/', documentation.include_docs_urls(title='Documentação funcional da API')),
]

# media files in development
urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        urls.url(r'^__debug__/', urls.include(debug_toolbar.urls))
    ]
