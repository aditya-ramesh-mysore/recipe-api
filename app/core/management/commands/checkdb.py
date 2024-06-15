from django.core.management.base import BaseCommand, CommandError
from django.db.utils import OperationalError
from django.db import connection
import time

class Command(BaseCommand):
    # Command to check database connection
    def handle(self, *args, **options):
        connected = False
        i = 5
        while not connected and i >= 0:
            try:
                connection.ensure_connection()
                connected = True
                self.stdout.write("Database connection established")
                return
            except OperationalError:
                self.stdout.write("Database unavailable, trying again after 1 second")
                time.sleep(1)
            i = i - 1

        self.stdout.write("Could not connect to database")
