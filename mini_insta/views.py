# File: views.py
# Author: alexander chappuis (alexc26@bu.edu), 2/10/26
# Description: contains the views for two profile views

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Profile, Post, Photo, Like, Follow
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm, CreateProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User 
from django.contrib.auth import login   

class MyLoginRequiredMixin(LoginRequiredMixin):

    def get_login_url(self) -> str:
        '''get the url for the login page.'''
        return reverse('login')

    def get_logged_in_profile(self):
        '''get the profile with the user that is logged in'''
        return Profile.objects.get(user=self.request.user)




class ProfileListView(ListView):
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = "profiles"



class ProfileDetailView(DetailView):
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        '''override for following logic'''
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            my_profile = Profile.objects.filter(user=self.request.user).first()
            if my_profile:
                context['is_following'] = Follow.objects.filter(
                    profile=self.get_object(), follower_profile=my_profile
                ).exists()
                context['is_own_profile'] = (my_profile == self.get_object())
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = 'post'





class CreatePostView(MyLoginRequiredMixin,CreateView):
    '''handle creation of a new Post.'''


    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self):
        '''return context variables.'''

        context = super().get_context_data()
        pk = self.kwargs['pk']
        profile = self.get_logged_in_profile()
        context['profile'] = profile
        return context

    def form_valid(self, form):
        ''' form submission  '''

        print(f"CreatePostView.form_valid: form.cleaned_data={form.cleaned_data}")

        pk = self.get_logged_in_profile()
        profile = Profile.objects.get(pk=pk)

        form.instance.profile = profile 

        saved = super().form_valid(form)

        image_url = self.request.POST.get('image_url', '')
        if image_url: 
            Photo.objects.create(post=self.object, image_url=image_url)

        return saved

        #require login


    def get_success_url(self):
        '''after submitting the post go to the submission'''
        return reverse('show_post', kwargs={'pk': self.object.pk})

class UpdateProfileView(MyLoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"
    def get_object(self):
        '''get the profile using the custom mixin'''
        return self.get_logged_in_profile()



class UpdatePostView(MyLoginRequiredMixin,UpdateView):
    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"



class DeletePostView(MyLoginRequiredMixin, DeleteView):
    '''delete post'''
    model = Post
    template_name = "mini_insta/delete_post_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['post'] = post
        context['profile'] = post.profile
        return context

    def get_success_url(self):
        post = self.get_object()
        return reverse('show_profile', kwargs={'pk': post.profile.pk})


class ShowFollowersDetailView(DetailView):
    '''show followers'''
    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = 'profile'


class ShowFollowingDetailView(DetailView):

    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = 'profile'

class PostFeedListView(MyLoginRequiredMixin, ListView):
    '''view for post feed'''
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        profile = self.get_logged_in_profile()
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_logged_in_profile()
        return context


class SearchView(MyLoginRequiredMixin, ListView):
    '''handles search for Profiles and Posts.'''

    template_name = "mini_insta/search_results.html"
    context_object_name = "posts"

    def dispatch(self, request, *args, **kwargs):
        if 'query' not in self.request.GET:
            pk = self.get_logged_in_profile()
            profile = Profile.objects.get(pk=pk)
            return render(request, 'mini_insta/search.html', {'profile': profile})
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        return Post.objects.filter(caption__icontains=query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.get_logged_in_profile()
        query = self.request.GET.get('query', '')
        context['profile'] = Profile.objects.get(pk=pk)
        context['query'] = query
        profiles_by_username = list(Profile.objects.filter(username__icontains=query))
        profiles_by_name = list(Profile.objects.filter(display_name__icontains=query))
        profiles_by_bio = list(Profile.objects.filter(bio_text__icontains=query))
        all_profiles = []
        seen_keys = set()
        for profile in profiles_by_username + profiles_by_name + profiles_by_bio:
            if profile.pk not in seen_keys:
                all_profiles.append(profile)
                seen_keys.add(profile.pk)
        context['profiles'] = all_profiles
        return context
 
    def get_object(self):
            '''get the profile using the custom mixin'''
            return self.get_logged_in_profile()


class ShowOwnProfileView(MyLoginRequiredMixin, DetailView):
    '''show page of logged in user'''
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = 'profile'

    def get_object(self):
        return self.get_logged_in_profile()


class CreateProfileView(CreateView):
    '''creation of a new user and profile'''

    model = Profile
    form_class = CreateProfileForm
    template_name = "mini_insta/create_profile_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_creation_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        '''create user and log them in'''
        user_creation_form = UserCreationForm(self.request.POST)

        if not user_creation_form.is_valid():
            return self.render_to_response(
                self.get_context_data(form=form)
            )

        user = user_creation_form.save()

        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        form.instance.user = user

        return super().form_valid(form)

    def get_success_url(self):
        '''go to new profile'''
        return reverse('show_profile', kwargs={'pk': self.object.pk})


class FollowView(MyLoginRequiredMixin, TemplateView):
    ''' follow another profile.'''

    def dispatch(self, request, *args, **kwargs):
        '''Create a Follow relationship and redirect.'''
        other_profile = Profile.objects.get(pk=self.kwargs['pk'])
        my_profile = self.get_logged_in_profile()
        if my_profile != other_profile:
            Follow.objects.get_or_create(profile=other_profile, follower_profile=my_profile)
        return redirect('show_profile', pk=other_profile.pk)


class DeleteFollowView(MyLoginRequiredMixin, TemplateView):
    ''' unfollowing another profile.'''

    def dispatch(self, request, *args, **kwargs):
        '''Remove a Follow relationship and redirect.'''
        other_profile = Profile.objects.get(pk=self.kwargs['pk'])
        my_profile = self.get_logged_in_profile()
        Follow.objects.filter(profile=other_profile, follower_profile=my_profile).delete()
        return redirect('show_profile', pk=other_profile.pk)


class LikeView(MyLoginRequiredMixin, TemplateView):
    '''like a post.'''

    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        my_profile = self.get_logged_in_profile()
        if my_profile != post.profile:
            Like.objects.get_or_create(post=post, profile=my_profile)
        return redirect('show_post', pk=post.pk)


class DeleteLikeView(MyLoginRequiredMixin, TemplateView):
    '''unliking a post.'''

    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        my_profile = self.get_logged_in_profile()
        Like.objects.filter(post=post, profile=my_profile).delete()
        return redirect('show_post', pk=post.pk)