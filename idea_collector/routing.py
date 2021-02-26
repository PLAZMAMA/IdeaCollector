from django.urls import path
from idea.consumers import GetMostRecent

ws_urlpatterns = [
    path('ws/most_recent_ideas/', GetMostRecent.as_asgi())
]