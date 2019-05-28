"""Contém funções relacionadas ao carregamento de objetos."""

import importlib


def import_string(dotted_path):
    """Importa um objeto utilizando seu nome completamente qualificado."""
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)

    except ValueError as e:
        msg = '"{}" não é um módulo válido.'.format(dotted_path)
        raise ImportError(msg) from e

    module = importlib.import_module(module_path)

    try:
        return getattr(module, class_name)

    except AttributeError as e:
        msg = 'Módulo "{}" não define "{}" como um nome válido.'.format(module_path, class_name)
        raise ImportError(msg) from e
