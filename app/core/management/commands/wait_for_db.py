"""
Django command to wait for the database to be available.
"""
import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""

    # quando rodarmos o comando wait_for_db, esse é o método que será chamado
    def handle(self, *args, **options):
        """Entrypoint for command."""
        # escreve no console
        self.stdout.write('Waiting for database...')
        # bool var que diz se o database está funcionando. começa em false
        db_up = False
        # enquanto o database não estiver funcionando...
        while db_up is False:
            try:
                # aparentemente o comando abaixo faz o docker-compose iniciar
                # o database. qd faço `docker-compose` ps após rodar
                # `docker-compose run --rm app sh -c "python manage.py
                # wait_for_db` eu vejo o container do db rodando
                self.check(databases=['default'])
                # se funcionou, atualiza o bool. se não, exception
                db_up = True
            # caso ocorra uma dessas duas exceptions, sabemos que é pq o
            # database ainda não está pronto. Outras exceptions não são
            # pegas aqui
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
