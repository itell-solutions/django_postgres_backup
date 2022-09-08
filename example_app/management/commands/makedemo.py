from django.contrib.auth.models import User
from django.core.management import BaseCommand

from django_postgres_backup.common import ADMIN_USERNAME
from example_app.models import Cars
from example_project.settings import DEMO_PASSWORD

CARS_TO_CREATE = ["Audi", "Mercedes", "BMW"]


def makedemo():
    if not User.objects.filter(username=ADMIN_USERNAME).exists():
        print("Create super user")
        User.objects.create_superuser(ADMIN_USERNAME, password=DEMO_PASSWORD)
    print(f"Creating demo cars{CARS_TO_CREATE}")
    Cars.objects.bulk_create(Cars(name=name) for name in CARS_TO_CREATE)


class Command(BaseCommand):
    help = "Create demo names for example_app."

    def handle(self, *args, **options):
        makedemo()
