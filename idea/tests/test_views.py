from rest_framework.test import APITestCase, APIClient
from idea.models import IdeaModel
from idea_collector.settings import MEDIA_ROOT
import coreapi
import json


class TestIdea(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        IdeaModel.objects.all().delete()
    
    #get/list/retrieve
    def test_get(self):
        ideas = [IdeaModel.objects.create(title='test0', description='description0'), IdeaModel.objects.create(title='test1', description='description1')]

        #single
        byte_string = self.client.get(f'/ideas/{ideas[0].id}/').content
        response = json.loads(byte_string.decode())

        self.assertEqual(ideas[0].title, response['title'])
        self.assertEqual(ideas[0].description, response['description'])

        #all
        byte_string = self.client.get('/ideas/').content
        response = json.loads(byte_string.decode())
        for i in range(len(ideas)):
            self.assertEqual(ideas[i].title, response[i]['title'])
            self.assertEqual(ideas[i].description, response[i]['description'])

    #post/create
    def test_post(self):
        with open(f'{MEDIA_ROOT}/images/test_picture.jpeg', 'rb') as pic:
            byte_string = self.client.post('/ideas/', {"title": "test1", "description": "description1", "picture": pic}).content
            byte_string = byte_string.decode()

        uploaded_idea = IdeaModel.objects.get(id=json.loads(byte_string)['id'])
        self.assertEquals([uploaded_idea.title, uploaded_idea.description], ['test1', 'description1'])

    #put/update
    def test_put(self):
        idea = IdeaModel.objects.create(title='test1', description='description1', picture=None)
        with open(f'{MEDIA_ROOT}/images/test_picture.jpeg', 'rb') as pic:
            self.client.put(f'/ideas/{idea.id}/', {"title": "test2", "description": "description2", "picture": pic})#, content_type='multipart/form-data')

        changed_idea = IdeaModel.objects.get(id=idea.id)
        self.assertEqual(changed_idea.title, 'test2')
        self.assertEqual(changed_idea.description, 'description2')

    #delete/destroy
    def test_delete(self):
        idea = IdeaModel.objects.create(title='test1', description='description1')
        self.client.delete(f'/ideas/{idea.id}')
        