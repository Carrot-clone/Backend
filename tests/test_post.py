import pytest, json
from rest_framework.test import APIClient, APITestCase
from user.models import UserModel

# 게시글 더미 생성 및 체크
def making_and_checking_dummy_post(url, token, response):
    http_author = 'Bearer {}'.format(token)
    res = response.client.post(
        url,
        json.dumps({
            "title": "This is test title",
            "content": "Test content",
            "price" : 50000,
            "category" : "hot",
            "image" : "2.png"
        }),
        content_type="application/json",
        HTTP_AUTHORIZATION=http_author
    )
    assert res.status_code == 201

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
    
    # 메인 페이지 리스트 조회 (글 없음)
    def test_post_get_list_success(self):
        url = "/api/post/list/?page=1"
        http_author = 'Bearer {}'.format(self.token)
        res = self.client.get(
            url, {}, content_type="application/json", HTTP_AUTHORIZATION=http_author
        )
        assert res.status_code == 200
        assert res.data['results'] == []

    # 페이지 제작
    def test_post_make(self):
        url = "/api/post/"
        making_and_checking_dummy_post(url,self.token,self)

    # 페이지 상세 페이지 조회 (성공)
    def test_post_get_Detail_Exist(self):
        url = "/api/post/"
        making_and_checking_dummy_post(url,self.token,self)
        url_get = "/api/post/1/"
        http_author = 'Bearer {}'.format(self.token)
        res = self.client.get(
            url_get, {}, content_type="application/json", HTTP_AUTHORIZATION=http_author
        )
        assert res.status_code == 200

    # 메인 페이지 리스트 조회 (글 있음)
    def test_post_get_list_success(self):
        url_post = "/api/post/"
        making_and_checking_dummy_post(url_post,self.token,self)
        http_author = 'Bearer {}'.format(self.token)

        url = "/api/post/list/?page=1"
        res_get = self.client.get(
            url, {}, content_type="application/json", HTTP_AUTHORIZATION=http_author
        )
        assert res_get.status_code == 200
        assert res_get.data['results'] != []