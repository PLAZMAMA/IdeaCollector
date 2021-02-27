from rest_framework.viewsets import ModelViewSet
from idea.models import IdeaModel
from idea.serializers import IdeaSerializer
from idea.tasks import publish_most_recent_ideas
from idea_collector.celery import app
from idea_collector.settings import DEBUG

class IdeaViewSet(ModelViewSet):
    queryset = IdeaModel.objects.all()
    serializer_class = IdeaSerializer
    def create(self, request, *args, **kwargs):
        if not(DEBUG):
            publish_most_recent_ideas.delay()
            
        return super().create(request, args, kwargs)
    
    def update(self, request, *args, **kwargs):
        if not(DEBUG):
            publish_most_recent_ideas().delay()

        return super().update(request, args, kwargs)

    def delete(self, request, *args, **kwargs):
        if not(DEBUG):
            publish_most_recent_ideas().delay()

        return super().delete(request, args, kwargs)