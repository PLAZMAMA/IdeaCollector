from django.core.management.base import BaseCommand
from idea_collector.settings import BASE_DIR
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            crd_path = os.join.path(BASE_DIR, 'operator/idea-collector-crd')
            os.system(f'kubectl apply -f {crd_path}')
        
        except Exception as e:
            raise Exception(f'pipenv or kubectl are not installed properly: {e}')