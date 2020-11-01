from django.db import models
from datetime import datetime

class Idea(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=512)
    picture = models.ImageField(upload_to=f'images')

    def __str__(self):
        return f'{self.pk}, {self.title}, {self.description}, {self.picture}'