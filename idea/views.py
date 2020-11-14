from django.http import HttpResponseBadRequest
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.shortcuts import render
from idea.forms import IdeaForm
from idea.models import IdeaModel
import json
import logging


"""
/ideas/<id>/  singular(has id):
read-get
update-patch/put
delete-delete

/ideas/  plural:
create-post
read(plural)-get
"""

class IdeaView(ModelViewSet):
    def get(self, request, pk=None):
        """In a case where the id is given, it returns the idea that matched the provided id. Otherwise it returns all of the ideas in the database"""
        if id:
            chosen_idea = models.Idea.objects.get(id=id)
            return Response({'title': chosen_idea.title, 'description': chosen_idea.description, 'picture': f'/{chosen_idea.picture}'})

        
        ideas = [{'title': idea.title, 'description': idea.description, 'picture': f'127.0.0.1:8000/{idea.picture}'} for idea in models.Idea.objects.all()]
        return Response({'ideas': ideas})

    def post(self, request, pk=None):
        """If not given an id, it creates an object from the request body(POST, FILES)"""
        if id:
            return HttpResponseBadRequest('unneccesary id was given')

        else:
            try:
                idea = models.Idea.objects.create(title=request.POST['title'], description=request.POST['description'], picture = request.FILES['picture'])
                return Response({'idea_id': idea.id})

            except:
                return HttpResponseBadRequest('the required arguments were not given or not given properly')

    def put(self, request, pk=None):
        """If given an id, it modifies the whole idea with the matching id"""
        #logging.critical(request.body)
        if id:
            logging.critical('initiated')
            #try:
            body = json.loads(request.body.decode())
            selected_idea = models.Idea.objects.get(id=id)
            logging.critical('start')
            selected_idea.title = body['title']
            logging.critical('getting there')
                #selected_idea.description = request.body['description']
                #selected_idea.picture = request.body['picture']
            logging.critical('working')
            selected_idea.save()
            logging.critical(selected_idea)
            #except:
            #    return HttpResponseBadRequest('all of the required arguments were not given or not given properly')

        else:
            return HttpResponseBadRequest('an id wasnt given')

    def patch(self, request, pk=None):
        """If given an id, it modifies the only the provided changes idea with the matching id"""
        if id:
            try:
                req_dict = request.PATCH.dict()
                files_dict = request.FILES.dict()
                chosen_idea = models.Idea.get(id=id)
                if 'title' in req_dict:
                    chosen_idea.title = req_dict['title']
                
                if 'description' in req_dict:
                    chosen_idea.description = req_dict['description']

                if 'picture' in files_dict:
                    chosen_idea.picture = files_dict['picture']
            
            except:
                return HttpResponseBadRequest('not given properly')
        else:
            return HttpResponseBadRequest('id was not found')

    def delete(self, request, pk=None):
        """When given an id, it deletes the idea with a matching id. Otherwise it deletes all of the ideas"""
        if id != '':
            try:
                models.Idea.objects.get(id=id).delete()
            
            except:
                return HttpResponseBadRequest('id was not found')
        
        else:
            Idea.objects.all().delete()