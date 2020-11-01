from django.contrib import admin
from idea.models import Idea

class IdeaAdmin(admin.ModelAdmin):
    pass

admin.site.register(Idea, IdeaAdmin)
