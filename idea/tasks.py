from celery import shared_task
from idea.models import IdeaModel
from channels.layers import get_channel_layer
from time import sleep

channel_layer = get_channel_layer()

@shared_task
def get_most_recent_ideas(num_of_ideas, most_recent_ideas):
    """gets the most recent "num_of_ideas""""
    last_most_recent_ideas = most_recent_ideas
    while(last_most_recent_ideas != most_recent_ideas):
        most_recent_ideas = IdeaModel.objects.all().order_by('-date')[:num_of_ideas:-1]
        sleep(3)
    
    return(most_recent_ideas)
    