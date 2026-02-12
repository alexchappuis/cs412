from django.shortcuts import render
from django.views.generic import ListView
from .models import Profile

# Create your views here.


class ProfileListView(ListView):

    model = Profile

    template_name = 'profile/show_all_profiles.html'

    context_object_name = "profiles"