from rest_framework.test import APITestCase
from idea.models import Idea
from idea_collector.settings import MEDIA_ROOT
from rest_framework.test import APIClient
import json

class TestIdea(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        Idea.objects.all().delete()

    def test_get(self):
        ideas = [Idea.objects.create(title='test0', description='description0'), Idea.objects.create(title='test1', description='description1')]
        #single
        binary = self.client.get(f'/ideas/{ideas[0].id}/').content
        response = json.loads(binary.decode())

        self.assertEqual(ideas[0].title, response['title'])
        self.assertEqual(ideas[0].description, response['description'])

        #all
        binary = self.client.get('/ideas/').content
        response = json.loads(binary.decode())
        for i in range(len(ideas)):
            self.assertEqual(ideas[i].title, response['ideas'][i]['title'])
            self.assertEqual(ideas[i].description, response['ideas'][i]['description'])

    def test_post(self):
        with open(f'{MEDIA_ROOT}/images/test_picture.jpeg', 'rb') as pic:
            binary = self.client.post('/ideas/', {'title': 'test1', 'description': 'description1', 'picture': pic }).content
            binary = binary.decode()

        uploaded_idea = Idea.objects.get(id=json.loads(binary)['idea_id'])
        self.assertEquals([uploaded_idea.title, uploaded_idea.description], ['test1', 'description1'])

    def test_put(self):
        idea = Idea.objects.create(title='test1', description='description1')
        idea.id = 10
        idea.save()
        with open(f'{MEDIA_ROOT}/images/test_picture.jpeg', 'rb') as pic:
            self.client.put('/ideas/10/', {'title': 'test2', 'description': 'description2', 'picture': pic})

        changed_idea = Idea.objects.get(id=10)
        self.assertEqual(changed_idea.title, 'test2')
        self.assertEqual(changed_idea.description, 'description2')

    def test_patch(self):
        idea = Idea.objects.create(title='test1', description='description1')
        idea.id = 20
        idea.save()
        self.client.patch('/ideas/20/', {'description': 'description2'})
        changed_idea = Idea.objects.get(id=20)
        self.assertEqual(changed_idea.title, 'test2')
        self.assertEqual(changed_idea.description, 'description2')

    def test_delete(self):
        self.client.delete('/ideas/1')
        