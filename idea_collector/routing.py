from django.urls import path
from idea.consumers import GetMostRecent, GetRandomIdea

ws_urlpatterns = [
    path('ws/most_recent_ideas/', GetMostRecent.as_asgi()),
    path('ws/get_random_idea/', GetRandomIdea.as_asgi())
]