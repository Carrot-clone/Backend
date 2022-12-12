import pytest, json
from rest_framework.test import APIClient, APITestCase
from user.models import UserModel
from django.core.files.uploadedfile import SimpleUploadedFile

class ClientRequest:
    def __init__(self, client):
        self.client = client

    def __call__(self, type, url, data=None):
        content_type = "application/json"

        if type == "get":
            res = self.client.get(
                url, {}, content_type=content_type
            )
        elif type == "post":
            res = self.client.post(
                url,
                json.dumps(data),
                content_type=content_type
            )
        elif type == "delete":
            res = self.client.delete(
                url, {}, content_type=content_type
            )
        else:
            res = self.client.put(
                url,
                json.dumps(data),
                content_type=content_type
            )
        return res


class TestView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.c = ClientRequest(self.client)

        # 유저 더미 생성
        self.password = "password"
        self.user = UserModel.objects.create_user(
            username='test',
            email='test@test.com',
            profilePhoto='url',
            password=self.password,
        )
        self.user.set_password(self.password)
        self.user.save()

        url = '/api/user/signin/'
        res = self.client.post(
            url,
            json.dumps({"email": "test@test.com", "password": "password"}),
            content_type="application/json"
        )
        self.token = res.data['accessToken']
    
    # 회원가입
    def test_user_signup(self):
        url = '/api/user/signup/'
        res = self.client.post(
            url,
            json.dumps({
            "email":"testsignup@test.com",
            "username":"testing",
            "password":"testing",
            }),
            content_type="application/json")
        assert res.status_code == 202

    # 이메일 체크
    def test_user_check(self):
        url_check = '/api/user/check/'
        res_check = self.client.post(
            url_check,
            json.dumps({
            "email":"test@test.com",
            }),
            content_type="application/json")
        assert res_check.status_code == 400

    # 로그인
    def test_user_login(self):
        url = '/api/user/signin/'
        res = self.client.post(
            url,
            json.dumps({
            "email":"test@test.com",
            "password": "password"
            }),
            content_type="application/json")
        assert res.status_code == 200