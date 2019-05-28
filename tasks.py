#!/usr/bin/env python3
"""Tarefas administrativas."""

import invoke


@invoke.task(default=True)
def run_server(ctx, noinput=True, clear=False, verbosity=0, settings='development', port=8000):
    """Executa o servidor web."""
    collectstatic(ctx, noinput, clear, verbosity, settings)
    cmd = f'./manage.py runserver 0.0.0.0:{port} --settings=questionario.settings.{settings}'
    ctx.run(cmd, echo=True, pty=True)


@invoke.task
def test(ctx, package='', settings='test'):
    """Testa as aplicações do projeto (com exceção dos testes funcionais)."""
    cmd = f'coverage run ./manage.py test {package} --settings=questionario.settings.{settings}'
    ctx.run(cmd, echo=True, pty=True)
    cmd = 'coverage report'
    ctx.run(cmd, echo=True, pty=True)


@invoke.task
def functional_tests(ctx, package='functional_tests.histories', settings='test'):
    """Executa os testes funcionais."""
    collectstatic(ctx, settings, True)
    cmd = f'coverage run ./manage.py test {package} . --settings=questionario.settings.{settings}'
    ctx.run(cmd, echo=True, pty=True)
    cmd = 'coverage report'
    ctx.run(cmd, echo=True, pty=True)


@invoke.task
def collectstatic(ctx, noinput=True, clear=False, verbosity=0, settings='development'):
    """Coleta arquivos estáticos."""
    ctx.run('yarn install', echo=True, pty=True)
    noinput = '--noinput' if noinput else ''
    clear = '--clear' if clear else ''
    cmd = f'./manage.py collectstatic {noinput} {clear} --verbosity={verbosity} '
    cmd += f'--settings=questionario.settings.{settings}'
    ctx.run(cmd, echo=True, pty=True)


@invoke.task
def make_migrations(ctx):
    """Gera migrações."""
    ctx.run('./manage.py makemigrations')


@invoke.task
def migrate(ctx):
    """Executa as migrações."""
    ctx.run('./manage.py migrate')
