from django.urls import path
from django.contrib.auth import views as auth_views    ## NEW
from .views import * # our view class definition 
urlpatterns = [
   path('', ShowAllView.as_view(), name='show_all'),
    path('article/<int:pk>', ArticleView.as_view(), name='article'),  # missing!
    path('article/create', CreateArticleView.as_view(), name="create_article"),
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name='create_comment'),
    path('article/<int:pk>/update', UpdateArticleView.as_view(), name="update_article" )
    path('comment/<int:pk', DeleteCommentView.as_view(), name="delete_comment")
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'), ## NEW
	path('logout/', auth_views.LogoutView.as_view(next_page='show_all'), name='logout'), ## NEW
    path('register/', RegistrationView.as_view(), name='register'),
    path("profile/", ShowOwnProfileView.as_view(), name="show_own_profile"),
]