from django.http import JsonResponse, HttpResponseBadRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from idea.forms import IdeaForm
import idea.models as models
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

class Idea(APIView):
    def get(self, request, id=None):
        """In a case where the id is given, it returns the idea that matched the provided id. Otherwise it returns all of the ideas in the database"""
        if id:
            chosen_idea = models.Idea.objects.get(id=id)
            return Response({'title': chosen_idea.title, 'description': chosen_idea.description, 'picture': f'/{chosen_idea.picture}'})

        
        ideas = [{'title': idea.title, 'description': idea.description, 'picture': f'127.0.0.1:8000/{idea.picture}'} for idea in models.Idea.objects.all()]
        return Response({'ideas': ideas})

    def post(self, request, id=None):
        """If not given an id, it creates an object from the request body(POST, FILES)"""
        if id:
            return HttpResponseBadRequest('unneccesary id was given')

        else:
            try:
                idea = models.Idea.objects.create(title=request.POST['title'], description=request.POST['description'], picture = request.FILES['picture'])
                return Response({'idea_id': idea.id})

            except:
                return HttpResponseBadRequest('the required arguments were not given or not given properly')

    def put(self, request, id=None):
        """If given an id, it modifies the whole idea with the matching id"""
        if id:
            try:
                selected_idea = models.Idea.objects.get(id=id)
                selected_idea.title = request.body['title']
                #selected_idea.description = request.body['description']
                #selected_idea.picture = request.body['picture']
                selected_idea.save()
            except:
                return HttpResponseBadRequest('all of the required arguments were not given or not given properly')

        else:
            return HttpResponseBadRequest('an id wasnt given')

    def patch(self, request, id=None):
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

    def delete(self, request, id=None):
        """When given an id, it deletes the idea with a matching id. Otherwise it deletes all of the ideas"""
        if id != '':
            try:
                models.Idea.objects.get(id=id).delete()
            
            except:
                return HttpResponseBadRequest('id was not found')
        
        else:
            Idea.objects.all().delete()