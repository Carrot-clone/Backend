from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializer import PostSerializer, PostListSerializer
from .models import PostModel
from django.http import Http404
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta

# Pagination
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

# Create your views here.
class PostCreateView(APIView):
    def post(self,request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(userId=request.user)
            return Response(data={"msg":"게시글 작성에 성공하셨습니다.", "status":200},status=200)
        return Response(data={"msg":"게시글 작성에 실패하셨습니다.", "status":400},status=400)

class PostListViewset(viewsets.ModelViewSet):
    queryset = PostModel.objects.all()
    serializer_class = PostListSerializer
    pagination_class = StandardResultsSetPagination
        

class PostDetailView(APIView):
    def get_object(self, pk):
        try:
            return PostModel.objects.get(pk=pk)
        except PostModel.DoesNotExist:
            raise Http404
   
    def get(self, request, pk):
        post = self.get_object(pk)
        if request.user in post.likeUsers.all():
            post.heartOn = 1
            post.save()
        else:
            post.heartOn = 0
            post.save()

        if request.user != post.userId:
            expire, current = datetime.now(), datetime.now()
            expire += timedelta(hours=5)
            expire -= current
            remain_time = expire.total_seconds()
            cookie_value = request.COOKIES.get('watch','_')
            serializer = PostSerializer(post)
            response_ = Response(serializer.data)
            if f'_{pk}_' not in cookie_value:
                cookie_value += f'{pk}_'
                response_.set_cookie('watch',value=cookie_value, max_age=remain_time, httponly=True)
                post.watchNumber += 1
                post.save()
            return response_
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if post.userId == request.user:
            if serializer.is_valid():
                serializer.save(userId=request.user)
                return Response({"status" : 200, "msg": "게시글 수정 성공"}, status=status.HTTP_202_ACCEPTED,)
            return Response({"status" : 400, "msg": "게시글 수정 실패"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"status" : 400, "msg": "게시글 수정 실패(작성유저와 수정유저가 불일치)"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        if post.userId == request.user:
            post.delete()
            return Response({"status" : 200, "msg": "게시글 삭제 성공"}, status=status.HTTP_204_NO_CONTENT,)
        return Response({"status" : 404, "msg": "게시글 삭제 실패 (작성유저와 삭제유저 불일치)"},status=status.HTTP_400_BAD_REQUEST)

class PostLikeView (APIView):
    def post(self, request, pk):
        post = get_object_or_404(PostModel,pk=pk)
        if request.user in post.likeUsers.all():
            post.likeUsers.remove(request.user)
            post.likeNumber -= 1
            post.save()
        else:
            post.likeUsers.add(request.user)
            post.likeNumber += 1
            post.save()
        return Response({"msg":"성공"})