from django.urls import path
from .views import * # our view class definition 

urlpatterns = [
    path('', ShowAllView.as_view(), name='show_all'), # generic class-based view
    path('article/create', CreateArticleView.as_view(), name="create_article"), # new
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name='create_comment'), ### NEW
]