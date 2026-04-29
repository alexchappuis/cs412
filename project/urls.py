from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'project'

urlpatterns = [

    # landing
    path('', views.LandingView.as_view(), name='landing'),

    # auth
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name='logout'),
    path('register/', views.CreateProfileView.as_view(), name='create_profile'),

    # trails
    path('trails/', views.TrailListView.as_view(), name='trail_list'),
    path('trails/<int:pk>/', views.TrailDetailView.as_view(), name='trail_detail'),
    path('trails/create/', views.TrailCreateView.as_view(), name='trail_create'),
    path('trails/<int:pk>/edit/', views.TrailUpdateView.as_view(), name='trail_update'),
    path('trails/<int:pk>/delete/', views.TrailDeleteView.as_view(), name='trail_delete'),

    # profile
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_update'),

    # gear
    path('gear/', views.GearListView.as_view(), name='gear_list'),
    path('gear/<int:pk>/', views.GearDetailView.as_view(), name='gear_detail'),
    path('gear/add/', views.GearCreateView.as_view(), name='gear_create'),
    path('gear/<int:pk>/edit/', views.GearUpdateView.as_view(), name='gear_update'),
    path('gear/<int:pk>/delete/', views.GearDeleteView.as_view(), name='gear_delete'),

    # trips
    path('trips/', views.TripListView.as_view(), name='trip_list'),
    path('trips/<int:pk>/', views.TripDetailView.as_view(), name='trip_detail'),
    path('trips/create/', views.TripCreateView.as_view(), name='trip_create'),
    path('trips/<int:pk>/edit/', views.TripUpdateView.as_view(), name='trip_update'),
    path('trips/<int:pk>/delete/', views.TripDeleteView.as_view(), name='trip_delete'),

    # pack list items
    path('trips/<int:trip_pk>/add-items/', views.add_pack_items, name='add_pack_items'),
    path('pack-item/<int:pk>/remove/', views.remove_pack_item, name='remove_pack_item'),
    path('pack-item/<int:pk>/toggle/', views.toggle_packed, name='toggle_packed'),

    # trip finder
    path('find/', views.trip_finder, name='trip_finder'),

]