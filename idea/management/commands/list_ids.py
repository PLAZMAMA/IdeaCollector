from django.core.management.base import BaseCommand
from idea.models import Idea

class Command(BaseCommand):
    def handle(self, *args, **options):
        for idea in Idea.objects.all():
            print(idea)