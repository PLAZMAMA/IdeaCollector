from django.urls import path
from idea.consumers import GetMostRecentIdea, GetRandomIdea, GetRandomIdeaChannels, GetMostRecentIdeasChannels

ws_urlpatterns = [
    path('ws/most_recent_ideas/', GetMostRecentIdea.as_asgi()),
    path('ws/get_random_idea/', GetRandomIdea.as_asgi()),
    path('ws/channels/most_recent_ideas/', GetRandomIdeaChannels.as_asgi()),
    path('ws/channels/get_random_idea/', GetMostRecentIdeasChannels.as_asgi()),
]