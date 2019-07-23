import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """ Djnago command to pause execution till databse is available """

    def handle(self, **args):
        self.stdout.write(' Waiting for database... ')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write(
                    'Database unavailable, Waiting for 1 sec ...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database Available!!!'))
