from django.core.management.base import BaseCommand
from idea.models import Idea

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-t', '--title', type=str, help='title of the idea', required=True)
        parser.add_argument('-b', '--body', type=str, help='body of the idea', required=True)
        
    def handle(self, *args, **options):
        idea = Idea.objects.create(title=options['title'], body=options['body'])
        
        #idea = Idea()
        #idea.title = options['title']
        #idea.body = options['body']
        #idea.save()

