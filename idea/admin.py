from django.contrib import admin
from idea.models import IdeaModel

class IdeaAdmin(admin.ModelAdmin):
    pass

admin.site.register(IdeaModel, IdeaAdmin)
