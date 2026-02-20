from django import forms
from .models import *


class CreatePostForm(forms.ModelForm):
    '''A form to add an Article to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        image_url = forms.URLField(required=False, label="Image URL")

        model = Post
        fields = ['caption']