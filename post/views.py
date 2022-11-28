from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import PostSerializer
from .models import UserModel
from django.utils import timezone

# Create your views here.
class PostingView(APIView):
    def post(self,request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(userId=request.user)
            return Response(data={"msg":"게시글 작성에 성공하셨습니다.", "status":200},status=200)
        return Response(data={"msg":"게시글 작성에 실패하셨습니다.", "status":400},status=400)