from rest_framework.viewsets import ModelViewSet
from idea.models import IdeaModel
from idea.serializers import IdeaSerializer

class IdeaViewSet(ModelViewSet):
    queryset = IdeaModel.objects.all()
    serializer_class = IdeaSerializer