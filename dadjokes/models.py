from django.db import models

# Create your models here.


class Joke(models.Model):
    joke = models.TextField()
    jokester = models.CharField()
    joke_time = models.DateTimeField()
    def __str__(self):
        return f'"{self.joke}" - {self.jokester}'


class Picture(models.Model):
    image_url = models.URLField()
    jokester = models.CharField()
    joke_time = models.DateTimeField()
    def __str__(self):
        return f'{self.image_url} - {self.jokester}'
