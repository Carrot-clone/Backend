from django.db import models
from user.models import UserModel
from django.utils import timezone
from datetime import datetime


def image_upload_path(instance, filename):
    t = datetime.now()
    return f"postImage/{instance.post_id.postId}/{t.second}_{t.microsecond}_{filename}"


# Create your models here.


class PostModel(models.Model):
    postId = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
    )
    userId = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        db_column="userId",
        null=True,
        related_name="userId",
    )
    price = models.BigIntegerField()
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    category = models.CharField(max_length=20)
    likeUsers = models.ManyToManyField(UserModel, related_name="likeUsers")
    heartOn = models.BooleanField(default=0)
    myPost = models.BooleanField(default=0)
    likeNumber = models.PositiveIntegerField(default=0)
    watchNumber = models.PositiveIntegerField(default=0)
    createdAt = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self


class PostImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    post_id = models.ForeignKey(
        PostModel, on_delete=models.CASCADE, related_name="image"
    )
    image = models.ImageField(upload_to=image_upload_path)

    def __int__(self):
        return self.id
