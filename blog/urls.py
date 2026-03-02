from django.urls import path
from .views import * # our view class definition 

urlpatterns = [
   path('', ShowAllView.as_view(), name='show_all'),
    path('article/<int:pk>', ArticleView.as_view(), name='article'),  # missing!
    path('article/create', CreateArticleView.as_view(), name="create_article"),
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name='create_comment'),
    path('article/<int:pk>/update', UpdateArticleView.as_view(), name="update_article" )
    path('comment/<int:pk', DeleteCommentView.as_view(), name="delete_comment")
    

]