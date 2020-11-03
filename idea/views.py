from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View
from django.shortcuts import render
from idea.forms import IdeaForm
import idea.models as models
from django.views.decorators.csrf import csrf_exempt


"""
/ideas/<id>/  singular(has id):
read-get
update-patch/put
delete-delete

/ideas/  plural:
create-post
read(plural)-get
"""

class Idea(View):
    def get(self, request, id=None):
        """In a case where the id is given, it returns the idea that matched the provided id. Otherwise it returns all of the ideas in the database"""
        if id:
            chosen_idea = models.Idea.objects.get(id=id)
            return JsonResponse({'title': chosen_idea.title, 'description': chosen_idea.description, 'picture': f'127.0.0.1:8000/{chosen_idea.picture}'})

        
        ideas = [{'title': idea.title, 'description': idea.description, 'picture': f'127.0.0.1:8000/{idea.picture}'} for idea in models.Idea.objects.all()]
        return JsonResponse({'ideas': ideas})

    def post(self, request, id=None):
        """If not given an id, it creates an object from the request body(POST, FILES)"""
        if id != '':
            return HttpResponseBadRequest('unneccesary id was given')

        else:
            try:
                models.Idea.objects.create(title=request.POST['title'], description=request.POST['description'], picture = request.FILES['picture'])

            except:
                return HttpResponseBadRequest('the required arguments were not given or not given properly')

    def put(self, request, id=None):
        """If given an id, it modifies the whole idea with the matching id"""
        if id != '':
            try:
                selected_idea = models.Idea.objects.get(id=id)
                selected_idea.title = request.PUT['title']
                selected_idea.title = request.PUT['description']
                selected_idea.title = request.FILES['picture']
                selected_idea.save()
            
            except:
                return HttpResponseBadRequest('all of the required arguments were not given or not given properly')

        else:
            return HttpResponseBadRequest('an id wasnt given')

    def patch(self, request, id=None):
        """If given an id, it modifies the only the provided changes idea with the matching id"""
        if id != '':
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


# class CreateIdea(View):
#     def get(self, request):
#         """returns a form that can be used to create an idea"""
#         return render(request, 'idea/input_idea.html', {'form': IdeaForm})

#     def post(self, request):
#         """creates an idea from the forms data and saves it to the database"""
#         idea_form = IdeaForm(request.POST, request.FILES)
#         if idea_form.is_valid():
#             idea = Idea.objects.create(title=idea_form.cleaned_data['title'], description=idea_form.cleaned_data['description'], picture=idea_form.cleaned_data['picture'])
#             success = True

#         else:
#             idea = None
#             success = False

#         return JsonResponse({'uploaded_idea': str(idea), 'uploaded_successfully': success, 'pic_url': idea.picture.url})

# class GetIdea(View):
#     def get(self, request, identifier=None):
#         """returns a single idea's primary key, title and description in json format or multiple ideas if they all match the given identifier"""
#         if type(identifier) == str:
#             ideas = [[idea.id, idea.title, idea.description, idea.picture] for idea in Idea.objects.filter(title=identifier)]

#         else:
#             ideas = Idea.objects.get(id=identifier)
#             ideas = [[ideas.id, ideas.title, ideas.description, ideas.picture]]
        
#         return JsonResponse({'idea': ideas})
    
# class GetIdeas(View):
#     def get(self, request):
#         """returns a list of all the ideas primary keys, titles and descriptions in json format"""
#         ideas = [[idea.id, idea.title, idea.description, idea.picture] for idea in Idea.objects.all()]
#         return JsonResponse({'ideas': ideas})

# class DeleteIdea(View):
#     def get(self, request, identifier=None):
#         """deletes a single idea's primary key, title and description in json format or multiple ideas if they all match the given identifier"""




#         """
#         if type(identifier) == str:
#             ideas = []
#             for idea in Idea.objects.filter(title=identifier):
#                 img = Image.open(f'{MEDIA_ROOT}/{idea.picture}')
#                 img_64 = b64encode(img.tobytes())
#                 ideas.append([idea.id, idea.title, idea.description, str(img_64)])
#                 Idea.objects

                
#             #ideas = [[idea.id, idea.title, idea.description, idea.picture] for idea in Idea.objects.filter(title=identifier)]

#         else:
#             ideas = Idea.objects.get(id=identifier).delete()
#             ideas = [[ideas.id, ideas.title, ideas.description, ideas.picture]]
        

#         return JsonResponse({'items_deleted': ideas})
#         """

# class ClearIdeas(View):
#     def get(self, request):
#         """deletes all the ideas that are in the database"""
#         ideas = [[idea.id, idea.title, idea.description, ideas.picture] for idea in Idea.objects.all().delete()]
#         return JsonResponse({'items_deleted': ideas})



