from django.urls import path, register_converter, re_path
from idea.views import IdeaViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register('', IdeaViewSet)
urlpatterns = router.urls