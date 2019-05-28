"""Testa o módulo loading."""

import unittest

from .. import loading


class LoadingTests(unittest.TestCase):
    """Testes de importação de objetos."""

    def test_import_module(self):
        """Verifica se um objeto é importado corretamente."""
        join = loading.import_string('os.path.join')
        self.assertIsNotNone(join)
        self.assertEqual(join('a', 'b'), 'a/b')

    def test_import_module_path_error(self):
        """Verifica se é lançada uma exceção para um módulo definido incorretamente."""
        with self.assertRaises(ImportError) as exc:
            loading.import_string('incorrect module')

        self.assertIsInstance(exc.exception.__cause__, ValueError)
        self.assertEqual(exc.exception.args[0], '"incorrect module" não é um módulo válido.')

    def test_import_module_object_error(self):
        """Verifica se é lançada uma exceção para um objeto não definido em um módulo."""
        with self.assertRaises(ImportError) as exc:
            loading.import_string('os.path.not_exist')

        self.assertIsInstance(exc.exception.__cause__, AttributeError)
        self.assertEqual(
            exc.exception.args[0],
            'Módulo "os.path" não define "not_exist" como um nome válido.'
        )
