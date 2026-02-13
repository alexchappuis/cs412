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

