import kopf
import pykube
import yaml
import inspect

@kopf.on.create('idea-collectors')
def idea_collector(body, **kwargs):
    deployment_configs = [
        {
        'name': 'web', 'replicas': body['spec']['web_app_replicas'],
        'command': '["pipenv run python manage.py makemigrations && pipenv run python manage.py migrate && pipenv run daphne -p 8080 -b 0.0.0.0 idea_collector.asgi:application"]'
        },
        {
        'name': 'celery', 
        'replicas': body['spec']['celery_worker_replicas'], 
        'command': '["pipenv run celery -A idea_collector worker --loglevel=INFO"]'
        },
        ]
    api = pykube.HTTPClient(pykube.KubeConfig.from_file())
    for deployment_config in deployment_configs:
        deployment_data = yaml.full_load(f"""
            apiVersion: apps/v1
            kind: Deployment
            metadata:
              name: idea-collector-{deployment_config['name']}
              labels:
                app: idea-collector-{deployment_config['name']}
            spec:
              replicas: {deployment_config['replicas']}
              selector:
                matchLabels:
                  app: idea-collector-{deployment_config['name']}
              template:
                metadata:
                  labels:
                    app: idea-collector-{deployment_config['name']}
                spec:
                  containers:
                  - name: idea-collector-{deployment_config['name']}
                    image: maorc112/idea_collector_web:latest
                    command: 
                    args: {deployment_config['command']}
                    ports:
                    - containerPort: 8080
                    env:
                    - name: POSTGRESQLUSERNAME
                      valueFrom:
                        secretKeyRef:
                          name: postgres-redis-credentials
                          key: username
                    - name: POSTGRESQLPASSWORD
                      valueFrom:
                        secretKeyRef:
                          name: postgres-redis-credentials
                          key: password
                    - name: POSTGRESQLHOST
                      valueFrom:
                        secretKeyRef:
                          name: postgres-redis-credentials
                          key: host
                    - name: REDIS_URL
                      valueFrom:
                        secretKeyRef:
                          name: postgres-redis-credentials
                          key: redis_url
            """)
        deployment = pykube.Deployment(api, deployment_data)
        deployment.create()

@kopf.on.update('idea-collectors')
def update_idea_colletor(body, **kwargs):
    pass