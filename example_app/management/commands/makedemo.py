from django.contrib.auth.models import User
from django.core.management import BaseCommand

from example_app.models import Cars
from example_project.settings import DEFAULT_DEMO_PASSWORD

CARS_TO_CREATE = ["Audi", "Mercedes", "BMW"]
ADMIN_USERNAME = "admin"


class Command(BaseCommand):
    help = "Create demo names for example_app."

    def handle(self, *args, **options):

        print("Create super user")
        if not User.objects.filter(username=ADMIN_USERNAME).exists:
            User.objects.create_superuser(ADMIN_USERNAME, password=DEFAULT_DEMO_PASSWORD)
        print(f"Creating demo cars{CARS_TO_CREATE}")
        Cars.objects.bulk_create(Cars(name=name) for name in CARS_TO_CREATE)
