import time
# to make a connection with the db
from django.db import connections
# a db error that we gonna return in case the db is not ready yet
from django.db.utils import OperationalError
# for creating the command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    # a callback that gets called whenever we call the command
    def handle(self, *args, **options):
        self.stdout.write("waiting for the db...")
        db_connection = None
        while not db_connection:
            try:
                # trying to connect to the default db
                db_connection = connections['default']
            # if not return OperationalError and then wait 1 second
            # and try again
            except OperationalError:
                self.stdout.write("db unavailable, waiting 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('DataBase available!'))
