# File: models.py
# Author: alexander chappuis (alexc26@bu.edu), 2/10/26
# Description: contains the models for storing data

from django.db import models
from django.contrib.auth.models import User

 
 
class Profile(models.Model):
    '''Tracks Profiles in the Mini Instagram.'''

    username = models.TextField(blank=False)
    display_name = models.TextField(blank=False)
    profile_image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)
    bio_text = models.TextField(blank=False)
    join_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 



    def __str__(self):
        return f'{self.username}'

    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})

    def get_all_posts(self):
        posts = Post.objects.filter(profile=self).order_by('-timestamp')
        return posts

    def get_followers(self):
        follows = Follow.objects.filter(profile=self)
        return [f.follower_profile for f in follows]

    def get_num_followers(self):
        return Follow.objects.filter(profile=self).count()

    def get_following(self):
        follows = Follow.objects.filter(follower_profile=self)
        return [f.profile for f in follows]

    def get_num_following(self):
        return Follow.objects.filter(follower_profile=self).count()

    def get_post_feed(self):
        following_profiles = self.get_following()
        posts = Post.objects.filter(profile__in=following_profiles).order_by('-timestamp')
        return posts


class Post(models.Model):
    '''Tracks posts.'''

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        return f'{self.profile}'

    def get_absolute_url(self):
        return reverse('show_post', kwargs={'pk': self.pk})

    def get_all_photos(self):
        photos = Photo.objects.filter(post=self)
        return photos

    def get_all_comments(self):
        return Comment.objects.filter(post=self).order_by('timestamp')

    def get_likes(self):
        return Like.objects.filter(post=self)

    def get_num_likes(self):
        return Like.objects.filter(post=self).count()




class Photo(models.Model):
    '''Tracks photos.'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.image_file:
            return f'Photo (file) for post {self.post.pk}'
        return f'Photo (url) for post {self.post.pk}'

    def get_image_url(self):
        if self.image_url:
            return self.image_url
        if self.image_file:
            return self.image_file.url
        return ''


class Follow(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.follower_profile.display_name} follows {self.profile.display_name}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=False)

    def __str__(self):
        return f'{self.profile.display_name} commented on post {self.post.pk}: {self.text[:30]}'


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.profile.display_name} likes post {self.post.pk}'

