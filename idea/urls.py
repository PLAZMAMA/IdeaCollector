from django.urls import path, register_converter, re_path
from idea.views import Idea
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', Idea.as_view()),
    re_path(r'^(?P<id>\w+)/$', Idea.as_view())
]
