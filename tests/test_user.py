import json
from rest_framework.test import APIClient, APITestCase
from user.models import UserModel


class ClientRequest:
    """
    A class with request of the client in REST API
    """

    def __init__(self, client):
        self.client = client

    def __call__(self, method, url, data=None):
        content_type = "application/json"

        if method == "get":
            res = self.client.get(url, {}, content_type=content_type)
        elif method == "post":
            res = self.client.post(url, json.dumps(data), content_type=content_type)
        elif method == "delete":
            res = self.client.delete(url, {}, content_type=content_type)
        else:
            res = self.client.put(url, json.dumps(data), content_type=content_type)
        return res


class TestView(APITestCase):
    """
    Testview for some functions : user's signup, checking-email and signin
    """

    def setUp(self):
        self.client = APIClient()
        self.client_request = ClientRequest(self.client)

        # 유저 더미 생성
        self.password = "password"
        self.user = UserModel.objects.create_user(
            username="test",
            email="test@test.com",
            profilePhoto="url",
            password=self.password,
        )
        self.user.set_password(self.password)
        self.user.save()

        url = "/api/user/signin/"
        res = self.client.post(
            url,
            json.dumps({"email": "test@test.com", "password": "password"}),
            content_type="application/json",
        )
        self.token = res.data["accessToken"]

    # 회원가입
    def test_user_signup(self):
        """
        Checking a function signup
        """
        url = "/api/user/signup/"
        res = self.client.post(
            url,
            json.dumps(
                {
                    "email": "testsignup@test.com",
                    "username": "testing",
                    "password": "testing",
                }
            ),
            content_type="application/json",
        )
        assert res.status_code == 202

    # 이메일 체크
    def test_user_check(self):
        """
        Checking a function of checking an email
        """
        url_check = "/api/user/check/"
        res_check = self.client.post(
            url_check,
            json.dumps(
                {
                    "email": "test@test.com",
                }
            ),
            content_type="application/json",
        )
        assert res_check.status_code == 400

    # 로그인
    def test_user_signin(self):
        """
        Checking a function of signin
        """
        url = "/api/user/signin/"
        res = self.client.post(
            url,
            json.dumps({"email": "test@test.com", "password": "password"}),
            content_type="application/json",
        )
        assert res.status_code == 200
