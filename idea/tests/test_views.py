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

    # def test_list(self):
        

    # def test_retrieve(self):
    #     pass

    # def test_create(self):
    #     pass

    # def test_update(self):
    #     pass

    # def test_partial_update(self):
    #     pass

    # def test_destroy(self):
    #     pass

    def test_get(self):
        ideas = [IdeaModel.objects.create(title='test0', description='description0'), IdeaModel.objects.create(title='test1', description='description1')]
        #single
        byte_string = self.client.get(f'/ideas/{ideas[0].id}/')#.content
        print(byte_string)
        #client = coreapi.Client()
        #print(client.get(f'https://http://0.0.0.0:8000/ideas/{ideas[0].id}'))
        #byte_string = client.get(f'https://127.0.0.1/ideas/{ideas[0].id}')
        #print(byte_string)
        #response = json.loads(byte_string.decode())

    #     self.assertEqual(ideas[0].title, response['title'])
    #     self.assertEqual(ideas[0].description, response['description'])

    #     #all
    #     byte_string = self.client.get('/ideas/').content
    #     response = json.loads(byte_string.decode())
    #     for i in range(len(ideas)):
    #         self.assertEqual(ideas[i].title, response['ideas'][i]['title'])
    #         self.assertEqual(ideas[i].description, response['ideas'][i]['description'])

    # def test_post(self):
    #     with open(f'{MEDIA_ROOT}/images/test_picture.jpeg', 'rb') as pic:
    #         byte_string = self.client.post('/ideas/', {"title": "test1", "description": "description1", "picture": pic }).content
    #         byte_string = byte_string.decode()

    #     uploaded_idea = Idea.objects.get(id=json.loads(byte_string)['idea_id'])
    #     self.assertEquals([uploaded_idea.title, uploaded_idea.description], ['test1', 'description1'])

    # def test_put(self):
    #     idea = Idea.objects.create(title='test1', description='description1')
    #     idea.id = 10
    #     idea.save()
    #     with open(f'{MEDIA_ROOT}/images/test_picture.jpeg', 'rb') as pic:
    #         self.client.put('/ideas/10/', {"title": "test2", "description": "description2", "picture": pic}, content_type='multipart/form-data')

    #     changed_idea = Idea.objects.get(id=10)
    #     self.assertEqual(changed_idea.title, 'test2')
    #     self.assertEqual(changed_idea.description, 'description2')

    # def test_patch(self):
    #     idea = Idea.objects.create(title='test1', description='description1')
    #     idea.id = 20
    #     idea.save()
    #     self.client.patch("/ideas/20/", {"description": "description2"})
    #     changed_idea = Idea.objects.get(id=20)
    #     self.assertEqual(changed_idea.title, 'test2')
    #     self.assertEqual(changed_idea.description, 'description2')

    # def test_delete(self):
    #     self.client.delete('/ideas/1')
        