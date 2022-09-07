from django.core.management import BaseCommand

from django_postgres_backup.common import makedemo


class Command(BaseCommand):
    help = "Create demo names for example_app."

    def handle(self, *args, **options):
        makedemo()
