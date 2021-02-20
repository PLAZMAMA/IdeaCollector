from django.db import models
from datetime import datetime

class IdeaModel(models.Model):
    title = models.CharField(max_length=128, null=True)
    description = models.TextField(max_length=512, null=True)
    picture = models.ImageField(upload_to=f'images', null=True)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}, {self.title}, {self.description}, {self.picture}'