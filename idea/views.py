from rest_framework.viewsets import ModelViewSet
from idea.models import IdeaModel
from idea.serializers import IdeaSerializer
from idea_collector.celery import app
from idea_collector.settings import DEBUG

class IdeaViewSet(ModelViewSet):
    queryset = IdeaModel.objects.all()
    serializer_class = IdeaSerializer
    def create(self, request, *args, **kwargs):
        if not(DEBUG):
            app.send_task('tasks.get_most_recent_ideas')
            
        return super().create(request, *args, **kwargs)