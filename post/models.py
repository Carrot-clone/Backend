from django.db import models
from user.models import UserModel
from django.utils import timezone

# Create your models here.

class PostImage(models.Model):
    imageId = models.BigAutoField(auto_created=True, primary_key=True,serialize=False)
    imageList = models.ImageField()

class PostModel(models.Model):
    postId = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
    )
    userId = models.ForeignKey(UserModel, on_delete=models.CASCADE, db_column='userId',null=True, related_name='userId')
    imageId = models.IntegerField(blank=True)
    category = models.CharField(max_length=20)
    likeUsers = models.ManyToManyField(UserModel, related_name='likeUsers')
    heartOn = models.BooleanField(default=0)
    likeNumber = models.PositiveIntegerField(default=0)
    price = models.BigIntegerField()
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    createdAt = models.DateTimeField(default=timezone.now)
    watch = models.IntegerField(default=0,blank=True)

    def __str__(self):
        return self

# class PostLike(models.Model):
#     postId = models.ForeignKey(PostModel, on_delete=models.CASCADE, primary_key=True)
#     userId = models.ForeignKey(UserModel)