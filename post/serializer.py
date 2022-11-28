from rest_framework import serializers
from .models import PostModel

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ['userId','imageId','category','price','title', 'content']
