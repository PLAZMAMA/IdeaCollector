from rest_framework.serializers import ModelSerializer
from idea.models import IdeaModel

class IdeaSerializer(ModelSerializer):
    class Meta:
        model = IdeaModel
        fields = ['id', 'title', 'description', 'picture']