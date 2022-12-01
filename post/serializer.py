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
        for image_data in image_set.getlist('image'):
            PostImage.objects.create(post_id=instance, image=image_data)
        return instance

class PostListSerializer(serializers.ModelSerializer):
    thumbImage = serializers.SerializerMethodField()
    class Meta:
        model = PostModel
        fields = ['postId','price','title', 'createdAt','likeNumber','thumbImage']

    def get_thumbImage(self, object):
        image = PostImage.objects.filter(post_id=object.postId)
        print(dir(image[0].image))
        return image[0].image.url
