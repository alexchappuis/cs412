# File: forms.py


from django import forms
from .models import *


class CreatePostForm(forms.ModelForm):
    '''A form to add an Article to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        image_url = forms.URLField(required=False, label="Image URL")

        model = Post
        fields = ['caption']



class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption']


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name', 'profile_image_url', 'image_file', 'bio_text']


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption']

class CreateProfileForm(forms.ModelForm):
    '''create a new profile.'''
    class Meta:
        model = Profile
        fields = ['username', 'display_name', 'bio_text', 'profile_image_url']