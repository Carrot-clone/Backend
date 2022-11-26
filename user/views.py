from .serializer import UserSignupSerializer, UserCheckSerializer, UserLoginSerializer
from django.db import IntegrityError
from rest_framework.views import APIView, Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class UserSignupView (APIView):
    def post(self, request):
        try:
            serializer = UserSignupSerializer(data=request.data) 
            if serializer.is_valid(raise_exception=True):
                user = serializer.save(request)
                RefreshToken.for_user(user)
                return Response({"msg" : ["회원가입에 성공하셨습니다"], "status" : 201}, status=201)
        except IntegrityError:
            return Response({"msg" : ["회원가입에 실패하셨습니다"], "status" : 202})

class UserCheckView (APIView):
    def post(self, request):
        serializer = UserCheckSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":["사용 가능한 이메일입니다"], "status":200})


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return Response({"msg": "로그인에 실패했습니다.","status" : 400}, status=status.HTTP_409_CONFLICT)

        response = {
            "status": 200,
            "msg" : "로그인에 성공하셨습니다.",
            "user" : str(serializer.validated_data['user']),
            "accessToken": serializer.validated_data["access"], # 시리얼라이저에서 받은 토큰 전달
            "refreshToken" : serializer.validated_data["refresh"]
        }

        return Response(response, status=status.HTTP_200_OK)