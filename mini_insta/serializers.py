from rest_framework import serializers
from .models import Profile, Post, Photo


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'username', 'display_name', 'profile_image_url', 'bio_text', 'join_date']

class PostSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(source='get_all_photos', many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'profile', 'caption', 'timestamp', 'photos']
        read_only_fields = ['profile', 'timestamp']

class PhotoSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['id', 'image_url']

    def get_image_url(self, obj):
        return obj.get_image_url()