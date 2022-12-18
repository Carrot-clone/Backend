import json
from rest_framework.test import APIClient, APITestCase
from user.models import UserModel
from django.core.files.uploadedfile import SimpleUploadedFile
from requests_toolbelt.multipart.encoder import MultipartEncoder



class ClientRequest:
    '''
    A class with request of the client in REST API
    '''
    def __init__(self, client):
        self.client = client

    def __call__(self, method, url, data=None, files=None ,content_type="application/json"):

        if method == "get":
            res = self.client.get(url, {}, content_type=content_type)
        elif method == "post":
            res = self.client.post(url, data, files, content_type=content_type)
        elif method == "delete":
            res = self.client.delete(url, data, content_type=content_type)
        else:
            res = self.client.put(url, data, files, content_type=content_type)
        return res

# 게시글 더미 생성 및 체크
def making_and_checking_dummy_post(token, test):
    ''' 
    making a dummy post and checking a post exists
    '''
    image = SimpleUploadedFile(
        name="3.png",
        content=open("tests/3.png",'rb').read(),
        content_type="image/png"
    )
    url = '/api/post'
    http_author = f"Bearer {token}"
    fields_data = {
        'title' : 'test',
        'content' : 'test',
        'price' : '777',
        'category' : 'hot',
        'image' : ("3.png",image,"image/png"),
        }
    data = MultipartEncoder(fields_data)
    res = test.client.post(
        url,
        data=data.to_string(),
        content_type=data.content_type,
        HTTP_AUTHORIZATION=http_author,
    )
    assert res.status_code == 201

class TestView(APITestCase):
    '''
    Testview for some functions : CRUD and some other functions
    '''
    def setUp(self):
        '''
        Setting API Client and making a dummy user
        '''
        self.client = APIClient()
        self.client_request = ClientRequest(self.client)

        # 유저 더미 생성
        self.password = "password"
        self.user = UserModel.objects.create_user(
            username="test",
            email="test@test.com",
            profilePhoto="2.png",
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

    # 페이지 제작 및 좋아요
    def test_post_make(self):
        '''
        Checking a function of create
        '''
        making_and_checking_dummy_post(self.token, self)
        http_author = f"Bearer {self.token}"
        url_get = "/api/post/list/?page=1"
        res_get = self.client.get(
            url_get, {}, content_type="application/json", HTTP_AUTHORIZATION=http_author
        )
        post_id = res_get.data["results"][0]["postId"]
        url_heart = f"/api/post/{post_id}/heart/"
        res = self.client.post(
            url_heart, {}, content_type="application/json", HTTP_AUTHORIZATION=http_author
        )
        assert res.status_code == 204
        

    # 페이지 상세 페이지 조회 (성공)
    def test_post_get_detail(self):
        '''
        Checking a function of read
        '''
        making_and_checking_dummy_post(self.token, self)
        url_get = "/api/post/3/"
        http_author = f"Bearer {self.token}"
        res = self.client.get(
            url_get, {}, content_type="application/json", HTTP_AUTHORIZATION=http_author
        )
        assert res.status_code == 200

    # 페이지 상세 페이지 수정 (성공)
    def test_post_put_detail(self):
        '''
        Checking a function of update
        '''
        making_and_checking_dummy_post(self.token, self)
        http_author = f"Bearer {self.token}"

        url_put = "/api/post/7/"
        res_get = self.client.get(
            "/api/post/list/?page=1", {}, content_type="application/json", HTTP_AUTHORIZATION=http_author
        )

        img_name = res_get.data['results'][0]['thumbImage'][72:]
        url_img_del = f"/api/post/7/{img_name}"


        res_image = self.client.delete(
            url_img_del,
            {},
            content_type="application/json",
            HTTP_AUTHORIZATION=http_author,
        )
        assert res_image.status_code == 200

        image = SimpleUploadedFile(
        name="2.png",
        content=open("tests/2.png",'rb').read(),
        content_type="image/png"
        )

        fields_data = {
            'title' : 'test',
            'content' : 'UPDATED',
            'price' : '777',
            'category' : 'hot',
            'image' : ("2.png",image,"image/png"),
            }
        data = MultipartEncoder(fields_data)

        res_put = self.client.put(
            url_put,
            data=data.to_string(),
            content_type=data.content_type,
            HTTP_AUTHORIZATION=http_author,
        )
        res_get = self.client.get(
            url_put, {}, content_type="application/json", HTTP_AUTHORIZATION=http_author
        )
        assert res_put.status_code == 202
        assert res_get.data['mainPost']['content'] == 'UPDATED'

    # 메인 페이지 리스트 조회 (글 있음)
    def test_post_get_list_exist(self):
        '''
        Checking a function of getting paginated lists
        '''
        making_and_checking_dummy_post(self.token, self)
        http_author = f"Bearer {self.token}"

        url = "/api/post/list/?page=1"
        res_get = self.client.get(
            url, {}, content_type="application/json", HTTP_AUTHORIZATION=http_author
        )
        assert res_get.status_code == 200
        assert res_get.data["results"] != []

    # 카테고리 조회
    def test_post_get_category(self):
        '''
        Checking a function of categorized search
        '''
        making_and_checking_dummy_post(self.token, self)
        http_author = f"Bearer {self.token}"

        url = "/api/post/category/list/?page=1&category=hot"
        res_get = self.client.get(
            url, {}, content_type="application/json", HTTP_AUTHORIZATION=http_author
        )
        assert res_get.status_code == 200
        assert res_get.data["results"] != []

    # 검색 기능 조회
    def test_post_get_search(self):
        '''
        Checking a function of search in title
        '''
        making_and_checking_dummy_post(self.token, self)
        http_author = f"Bearer {self.token}"

        url = "/api/post/list/?page=1&search=test"
        res_get = self.client.get(
            url, {}, content_type="application/json", HTTP_AUTHORIZATION=http_author
        )
        assert res_get.status_code == 200
        assert res_get.data["results"] != []

    # 페이지 상세 페이지 삭제 (성공)
    def test_post_delete_detail(self):
        '''
        Checking a function of delete
        '''
        making_and_checking_dummy_post(self.token, self)
        url_get = "/api/post/list/?page=1"
        http_author = f"Bearer {self.token}"
        res_get = self.client.get(
            url_get, {}, content_type="application/json", HTTP_AUTHORIZATION=http_author
        )
        post_id = res_get.data["results"][0]["postId"]
        url_delete = f"/api/post/{post_id}/"
        res = self.client.delete(
            url_delete,
            {},
            content_type="application/json",
            HTTP_AUTHORIZATION=http_author,
        )
        assert res.status_code == 200
