from django.core.management.base import BaseCommand
from idea_collector.settings import BASE_DIR
import os

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_arguments('-v', '--verbose', type=bool, help='boolean of whether to add the verbose argument to the kopf operator or not(default: False)', default=False)

    def handle(self, *args, **options):
        try:
            crd_path = os.join.path(BASE_DIR, 'operator/idea-collector-crd')
            kopf_path = os.join.path(BASE_DIR, 'operator/idea_collector_operator')
            os.system(f'kubectl apply -f {crd_path}')
            os.system(f'pipenv run kopf run {kopf_path}')
        
        except Exception as e:
            raise Exception(f'pipenv or kubectl are not installed properly: {e}')