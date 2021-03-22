from django.core.management.base import BaseCommand
from idea_collector.settings import BASE_DIR
import os

class Command(BaseCommand):
    help = 'creates a new idea_collector operator'

    def add_arguments(self, parser):
        parser.add_argument('-verb', '--verbose', type=bool, help='boolean of whether to add the verbose argument to the kopf operator or not(default: False)', default=True)

    def handle(self, *args, **options):
        try:
            crd_path = os.path.join(BASE_DIR, 'operator/idea-collector-crd.yaml')
            kopf_path = os.path.join(BASE_DIR, 'operator/idea_collector_operator.py')
            os.system(f'kubectl apply -f {crd_path}')
            if options['verbose']:
                os.system(f'pipenv run kopf run --verbose {kopf_path}')
            
            else:
                os.system(f'pipenv run kopf run {kopf_path}')
        
        except Exception as e:
            raise Exception(f'pipenv, kubectl or minikube are not installed properly: {e}')