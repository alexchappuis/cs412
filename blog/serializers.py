

#containes 1 or more serializer classes
from rest_framework import serializers
from .models import *

class ArticleSerializer(serializers.ModelSerializer)