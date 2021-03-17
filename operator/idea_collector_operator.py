import kopf
import pykube
import yaml
import os
import django
import sys
from django.template.loader import render_to_string

#getting django settings from settings.py file
sys.path.append(os.pardir)
sys.path.append(os.path.join(os.pardir, 'idea_collector/'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'idea_collector.settings')
django.setup()

@kopf.on.create('idea-collectors')
def idea_collector_create(body, **kwargs):
    #getting the deployment configs from the given spec
    deployment_configs = [
        {
        'name': 'web',
        'replicas': body['spec']['web_app_replicas'],
        'command': '["pipenv run python manage.py makemigrations && pipenv run python manage.py migrate && pipenv run daphne -p 8080 -b 0.0.0.0 idea_collector.asgi:application"]'
        },
        {
        'name': 'celery', 
        'replicas': body['spec']['celery_worker_replicas'], 
        'command': '["pipenv run celery -A idea_collector worker --loglevel=INFO"]'
        }
        ]

    #getting the api for the pykube client
    api = pykube.HTTPClient(pykube.KubeConfig.from_file())

    #looping on each config and creating a kubernetes resource from it
    for deployment_config in deployment_configs:
        rendered_deployment_data = render_to_string(os.path.join(os.path.abspath(os.getcwd()), 'operator/templates/deployment.yaml'), context=deployment_config)
        deployment_data = yaml.full_load(rendered_deployment_data)
        deployment = pykube.Deployment(api, deployment_data)
        deployment.create()

@kopf.on.update('idea-collectors')
def update_idea_colletor(body, **kwargs):
    pass