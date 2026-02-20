# File: models.py
# Author: alexander chappuis (alexc26@bu.edu), 2/10/26
# Description: contains the models for storing data

from django.db import models
 
 
class Profile(models.Model):
    '''Tracks Profiles in the Mini Instagram'''
 
 
    username = models.TextField(blank=False)
    display_name = models.TextField(blank=False)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=False)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return the name of the profile'''
        return f'{self.username}'
    
    def get_all_posts(self):
        '''Return all of the posts.'''

        posts = Post.objects.filter(profile=self).order_by('-timestamp')
        return posts

class Post(models.Model):
    '''Tracks posts'''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=True) 
    def __str__(self):
        '''Return the name of the profile of the post'''
        return f'{self.profile}'
    
    def get_all_photos(self):
        '''Return all of the photos.'''

        photos = Photo.objects.filter(post=self)
        return photos

class Photo(models.Model):
    '''Tracks photos'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return photos'''
        return f'Photo for post {self.post.pk}'

