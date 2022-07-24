"""
Test custom Django management commands.
"""
from unittest.mock import patch

# erro possível retornado  pelo postgres se tentamos conectar antes de ele
# estar pronto o erro depende de qual ponto do starting o postres está
from psycopg2 import OperationalError as Psycopg2OpError
# permite que chamemos um management command no teste
from django.core.management import call_command
# erro possível retornado  pelo postgres se tentamos conectar antes de ele
# estar pronto
from django.db.utils import OperationalError
# nao precisamos criar nenhum database set up behind the scenes, logo
# SimpleTestCase só queremos testar erros de conexão ao postgres, nao simular
# CRUD no database
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        call_command('wait_for_db')

        # verifica se chamamos o database que definimos em settings.py
        # como default
        patched_check.assert_called_once_with(databases=['default'])

    # substitui a sleep function por um magic mock object. Assim simulamos
    # que chamamos o sleep, mas não precisamos esperar
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        # mocking library: nas primeiras 2x que for chamado, raise exception
        # Psycopg2OpError. Nas 3 vezes seguintes, raise exception
        # OperationalError. Na 6a vez retorna True
        patched_check.side_effect = [Psycopg2OpError] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        # se chamamos o database menos de 6 vezes, é porque não fizemos
        # o handling exception corretamente nas primeiras 5
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
