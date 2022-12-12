from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserModel

User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    '''
    A serializer for the basic sign-up
    '''
    email = serializers.EmailField(required=True, max_length=50)
    username = serializers.CharField(required=True, max_length=30)
    password = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"}
    )
    profilePhoto = serializers.ImageField(required=False,use_url=True)
    location = serializers.CharField(default="null", max_length=30)

    class Meta:
        '''
        A serializer of user sign-up's Meta-class
        '''
        model = UserModel
        fields = ["id", "email", "username", "password", "profilePhoto", "location"]

    def save(self, request):
        user = super().save()
        user.email = self.validated_data["email"]
        user.set_password(self.validated_data["password"])
        user.save()
        return user

    def validate(self, attrs):
        email = attrs.get("email", None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"msg": "이미 존재하는 이메일입니다.", "status": 200})
        return attrs


class UserCheckSerializer(serializers.ModelSerializer):
    '''
    A serializer for only checking user
    '''
    class Meta:
        '''
        A Meta-class for checking user's email
        '''
        model = UserModel
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email", None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"msg": "이미 존재하는 이메일입니다.", "status": 200})
        return attrs


class UserLoginSerializer(serializers.Serializer):
    '''
    A serializer for sign-in
    '''
    email = serializers.EmailField(required=True, write_only=True, max_length=20)
    password = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"}
    )

    class Meta:
        '''
        A serializer of user sign-in's Meta-class
        '''
        model = User
        fields = ["email", "password"]

    def validate(self, attrs):
        email = attrs.get("email", None)
        password = attrs.get("password", None)

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise serializers.ValidationError({"msg": "틀린 비밀번호입니다."})
        else:
            raise serializers.ValidationError({"msg": "계정이 존재하지 않습니다."})
        token = RefreshToken.for_user(user)
        refresh = str(token)
        access = str(token.access_token)

        attrs = {"user": str(user), "refresh": refresh, "access": access}
        return attrs
