from celery import shared_task
from idea.models import IdeaModel

@shared_task
def show_ideas():
    IdeaModel.objects.all()