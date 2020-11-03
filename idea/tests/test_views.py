from django.test import TestCase
from idea.models import Idea

class TestIdea(TestCase):
    def tearDown(self):
        Idea.objects.all().delete()

    def test_get(self):
        idea1 = Idea.objects.create(title='test1', description='description1')
        idea2 = Idea.objects.create(title='test2', description='description2')
        
        #single
        response = self.client.get(f'/ideas/{idea1.id}/')
        self.assertEqual(idea1.title, response['idea']['title'])
        self.assertEqual(idea1.description, response['idea']['description'])

        #all
        response = self.client.get('/ideas/')

        self.assertEqual(f'test1, description1', f"{response['ideas'][0].title}, {response['ideas'][0].description}", f'test2, description2', f"{response['ideas'][1].title}, {response['ideas'][1].description}")

    def test_post(self):
        with open('idea_collector/media/images/test_picture.jpeg', 'r') as pic:
            self.client.post('127.0.0.1:8000/ideas/', {'title': 'test1', 'description': 'description1', 'picture': pic}, content_type='multipart/form-data')

        uploaded_idea = Idea.objects.get(id=1)
        self.assertEquals([uploaded_idea.title, uploaded_idea.description], ['test3', 'description3'])

    def test_put(self):
        Idea.objects.create(title='test1', description='description1')
        with open('idea_collector/media/images/test_picture.jpeg', 'r') as pic:
            self.client.put('127.0.0.1:8000/ideas/1', {'title': 'test2', 'description': 'description2', 'picture': pic}, content_type='multipart/form-data')
        changed_idea = Idea.objects.get(id=1)
        self.assertEquals([changed_idea.title, changed_idea.description], ['test2', 'description2'])

    def test_patch(self):
        Idea.objects.create(title='test1', description='description1')
        self.client.patch('127.0.0.1:8000/ideas/1', {'description': 'description2'})
        changed_idea = Idea.objects.get(id=1)
        self.assertEqual(changed_idea.description, 'description2')

    def test_delete(self):
        self.client.delete('127.0.0.1:8000/ideas/1')
        