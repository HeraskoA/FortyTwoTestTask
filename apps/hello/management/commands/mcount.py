from django.core.management.base import BaseCommand
from django.db.models import get_models


class Command(BaseCommand):
    help = "Prints count of models."

    def handle(self, *args, **options):
        for model in get_models():
            out = 'There are %d objects in %s model' % (
                model.objects.count(),
                model.__name__
                )
            self.stdout.write(out)
            self.stderr.write('error: ' + out)
            
