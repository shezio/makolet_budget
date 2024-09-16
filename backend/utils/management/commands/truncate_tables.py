from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Truncate all tables in the database'

    def handle(self, *args, **kwargs):
        tables = ['public.budget_budget', 'public.purchase']
        with connection.cursor() as cursor:
            for table in tables:
                try:
                    cursor.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;")
                    self.stdout.write(self.style.SUCCESS(f'Successfully truncated {table}'))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Could not truncate {table}: {e}'))
