# File: views.py
# Author: alexander chappuis (alexc26@bu.edu), 2/10/26
# Description: contains the views for two profile views

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile



class ProfileListView(ListView):
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = "profiles"



class ProfileDetailView(DetailView):
    '''Show the details for one Profile.'''
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = 'profile'