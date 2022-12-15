from os import environ
from datetime import datetime, timedelta
import boto3
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from .serializer import PostSerializer, PostListSerializer
from .models import PostModel, PostImage
from .pagination import CustomPagination

s3_client = boto3.client(
    "s3",
    aws_access_key_id=environ["AWS_ACCESS_KEY"],
    aws_secret_access_key=environ["AWS_SECRET_ACCESS_KEY"],
    region_name="ap-northeast-2",
)

# Create your views here.
class PostCreateView(APIView):
    '''
    A view for creating a post
    '''
    def post(self, request):
        # if 'multipart/form-data' not in request.content_type[:30]:
        #     return Response(data={"msg": "Content-type이 일치하지 않습니다"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = PostSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(userId=request.user)
            return Response(
                data={"msg": "게시글 작성에 성공하셨습니다."},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data={"msg" : "게시글 작성에 실패하셨습니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class PostListViewset(viewsets.ModelViewSet):
    '''
    A view for reading some posts in lists
    '''
    queryset = PostModel.objects.all().order_by("-createdAt")
    serializer_class = PostListSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter]
    search_fields = ("title",)


class PostCategoryView(generics.ListAPIView):
    '''
    A view for categorized searching posts
    '''
    serializer_class = PostListSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = PostModel.objects.all()
        category = self.request.query_params.get("category", None)
        if category is not None:
            queryset = queryset.filter(category=category)
        return queryset.order_by("-createdAt")


class PostDetailView(APIView):
    '''
    A view for reading a post
    '''
    def get_object(self, pk):
        try:
            return PostModel.objects.get(pk=pk)
        except PostModel.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        post = self.get_object(pk)
        post.myPost = request.user == post.userId
        if request.user in post.likeUsers.all():
            post.heartOn = 1
            post.save()
        else:
            post.heartOn = 0
            post.save()
        posts = PostModel.objects.filter(userId=post.userId)
        others = []
        for post_ in posts[:5]:
            if post_.postId != post.postId:
                tem_image = PostImage.objects.filter(post_id=post_.postId)
                try:
                    others.append(
                        {
                            "thumbImage": tem_image[0].image.url,
                            "postId": post_.postId,
                            "title": post_.title,
                            "price": post_.price,
                        }
                    )
                except IndexError:
                    others.append(
                        {
                            "thumbImage": None,
                            "postId": post_.postId,
                            "title": post_.title,
                            "price": post_.price,
                        }
                    )
                    pass
        if request.user != post.userId:
            expire, current = datetime.now(), datetime.now()
            expire += timedelta(hours=5)
            expire -= current
            remain_time = expire.total_seconds()
            cookie_value = request.COOKIES.get("watch", "_")
            serializer = PostSerializer(post)
            response_ = Response({"mainPost": serializer.data, "otherPosts": others})
            if f"_{pk}_" not in cookie_value:
                cookie_value += f"{pk}_"
                response_.set_cookie(
                    "watch", value=cookie_value, max_age=remain_time, httponly=True
                )
                post.watchNumber += 1
                post.save()
            return response_
        serializer = PostSerializer(post)
        return Response(
            {"mainPost": serializer.data, "otherPosts": others},
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        post = self.get_object(pk)
        if post.userId == request.user:
            serializer = PostSerializer(
                post, data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save(userId=request.user)
                return Response(
                    {"msg": "게시글 수정 성공"},
                    status=status.HTTP_202_ACCEPTED,
                )
            return Response({"msg": "게시글 수정 실패"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(
                {"msg": "게시글 수정 실패(작성유저와 수정유저가 불일치)"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        post = self.get_object(pk)
        if post.userId == request.user:
            images = PostImage.objects.filter(post_id=post.postId)
            for image in images:
                target = image.image
                key = f"{target}"
                s3_client.delete_object(Bucket="melon-market-bucket", Key=key)
            post.delete()
            return Response(
                {"msg": "게시글 삭제 성공"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"msg": "게시글 삭제 실패 (작성유저와 삭제유저 불일치)"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class PostLikeView(APIView):
    '''
    A view for a fuction of like
    '''
    def post(self, request, pk):
        post = get_object_or_404(PostModel, pk=pk)
        if request.user in post.likeUsers.all():
            post.likeUsers.remove(request.user)
            post.likeNumber -= 1
            post.save()
        else:
            post.likeUsers.add(request.user)
            post.likeNumber += 1
            post.save()
        return Response({"msg": "성공"}, status=status.HTTP_204_NO_CONTENT)

class PostImageUpdateView(APIView):
    '''
    A view for a function of updating images
    '''
    def delete(self, request, pk):
        post = get_object_or_404(PostModel,pk=pk)
        if request.user == post.userId:
            for img in request.data.get('img'):
                PostImage.objects.get(image=f"postImage/{pk}/{img}").delete()
            return Response({"msg":"성공"}, status=status.HTTP_200_OK)
        return Response({"msg":"유저 불일치"}, status=status.HTTP_401_UNAUTHORIZED)