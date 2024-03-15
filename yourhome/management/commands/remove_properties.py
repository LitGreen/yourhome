from django.core.management.base import BaseCommand
from yourhome.models import Property 

class Command(BaseCommand):
    help = 'Removes all properties'

    def handle(self, *args, **options):
        Property.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Successfully removed all properties'))

