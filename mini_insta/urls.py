# File: urls.py
# Author: alexander chappuis (alexc26@bu.edu), 2/10/26
# Description: URl paths

from django.urls import path
from .views import ProfileListView, ProfileDetailView

urlpatterns = [
    path("", ProfileListView.as_view(), name="show_all_profiles"),
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="show_profile"),
]