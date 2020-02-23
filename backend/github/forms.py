from django import forms
from .models import Repo

class RepoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['base_url'].widget.attrs['placeholder'] = 'Search Git Https://'

    class Meta:
        model = Repo
        fields = ['base_url']
