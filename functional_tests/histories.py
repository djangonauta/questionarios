"""
Módulo contendo testes funcionais.

Testes funcionais estão separados dos testes de aplicação já que estão relacionados ao projeto em si e não
a uma aplicação específica.
"""

from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from selenium.webdriver import Firefox


class FunctionalTests(LiveServerTestCase):
    """Base para os testes funcionais."""

    def setUp(self):
        """Inicializa serviços necessários para execução dos testes funcionais."""
        self.driver = Firefox()
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)

    def tearDown(self):
        """Finaliza serviços."""
        self.driver.close()

    def get_live_url(self, url_name):
        """Obtém url_name em relação ao servidor de testes."""
        return '{}{}'.format(self.live_server_url, reverse(url_name))
