from rest_framework import serializers
from .models import PostModel, PostImage

class PostImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = PostImage
        fields = ['image']

class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='userId.username',read_only=True)
    images = serializers.SerializerMethodField()

    def get_images(self, object):
        image = object.image.all()
        return PostImageSerializer(instance=image, many=True, context=self.context).data

    class Meta:
        model = PostModel
        fields = ['userId','username','images','category','price','title', 'content','createdAt','watchNumber','likeNumber','heartOn']
    
    def create(self, validated_data):
        instance = PostModel.objects.create(**validated_data)
        image_set = self.context['request'].FILES
        for image_data,x in zip(image_set.getlist('image'),range(len(image_set.getlist('image')))):
            PostImage.objects.create(post_id=instance, image=image_data)
            if x == 0:
                instance.thumbImage = image_data
                instance.save()
        return instance

class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ['postId','price','title', 'createdAt','likeNumber','thumbImage']

