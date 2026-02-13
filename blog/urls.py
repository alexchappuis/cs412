from django.urls import path
from .views import ShowAllView # our view class definition 

urlpatterns = [
    path('', ShowAllView.as_view(), name='show_all'), # generic class-based view
]