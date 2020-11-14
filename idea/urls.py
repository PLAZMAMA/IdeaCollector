from django.urls import path, register_converter, re_path
from idea.views import IdeaView
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'users', IdeaView)
urlpatterns = router.urls