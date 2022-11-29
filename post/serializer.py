from rest_framework import serializers
from .models import PostModel

class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='userId.username',read_only=True)
    class Meta:
        model = PostModel
        fields = ['userId','username','imageId','category','price','title', 'content','createdAt','watchNumber','likeNumber','heartOn']

class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ['postId','imageId','price','title', 'createdAt','likeNumber']
