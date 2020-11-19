from django import forms
from idea.models import IdeaModel

#class IdeaForm(forms.Form):
#    title = forms.CharField(max_length=150)
#    description = forms.CharField(max_length=10000)
#    picture = forms.ImageField(required=False, allow_empty_file=True)

class IdeaForm(forms.ModelForm):
    class Meta:
        model = IdeaModel
        fields = ['title', 'description', 'picture']