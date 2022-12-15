'''
Some serializers of the post and it's images
'''
from rest_framework import serializers
from .models import PostModel, PostImage


class PostImageSerializer(serializers.ModelSerializer):
    '''
    A serializer for handling some images
    '''
    image = serializers.ImageField(use_url=True)

    class Meta:
        '''
        PostImageSerializer's Meta-class
        '''
        model = PostImage
        fields = ["image"]


class PostSerializer(serializers.ModelSerializer):
    '''
    A serializer for the basic post
    '''
    username = serializers.CharField(source="userId.username", read_only=True)
    profilePhoto = serializers.ImageField(source="userId.profilePhoto", read_only=True)
    images = serializers.SerializerMethodField()
    myPost = serializers.BooleanField(default=0)

    def get_images(self, object):
        '''
        A fuction of getting multiple images
        '''
        image = object.image.all()
        return PostImageSerializer(instance=image, many=True, context=self.context).data

    class Meta:
        '''
        PostSerializer's Meta-class
        '''
        model = PostModel
        fields = [
            "userId",
            "username",
            "profilePhoto",
            "images",
            "category",
            "price",
            "title",
            "content",
            "createdAt",
            "watchNumber",
            "likeNumber",
            "heartOn",
            "myPost"
        ]

    def create(self, validated_data):
        '''
        Creating post with mapping and seperating images
        '''
        image_set = self.context["request"].FILES
        if len(image_set) == 0:
            raise serializers.ValidationError({"msg": "이미지가 없습니다"})
        instance = PostModel.objects.create(**validated_data)
        for image_data in image_set.getlist("image"):
            PostImage.objects.create(post_id=instance, image=image_data)
        return instance

    def update(self, instance, validated_data):
        '''
        Updating post with new images
        '''
        image_set = self.context["request"].FILES
        if len(image_set) == 0:
            raise serializers.ValidationError({"msg": "이미지가 없습니다"})
        instance.category = validated_data.get("category", instance.category)
        instance.price = validated_data.get("price", instance.price)
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.save()
        PostImage.objects.filter(post_id=instance).delete()
        for image_data in image_set.getlist("image"):
            PostImage.objects.create(post_id=instance, image=image_data)
        return instance


class PostListSerializer(serializers.ModelSerializer):
    '''
    A serializer for paginated lists
    '''
    thumbImage = serializers.SerializerMethodField()

    class Meta:
        '''
        PostListSerializer's Meta-class
        '''
        model = PostModel
        fields = ["postId", "price", "title", "createdAt", "likeNumber", "thumbImage"]

    def get_thumbImage(self, object):
        '''
        Extracting the first image of images
        '''
        image = PostImage.objects.filter(post_id=object)
        try:
            return image[0].image.url
        except IndexError:
            return
