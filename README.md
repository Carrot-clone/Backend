# <strong>Backend

[![Maintainability](https://api.codeclimate.com/v1/badges/203b7f73823c7e2b1567/maintainability)](https://codeclimate.com/github/DongGuk-Seo/Backend/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/203b7f73823c7e2b1567/test_coverage)](https://codeclimate.com/github/DongGuk-Seo/Backend/test_coverage)
<br>
<br>

## 🖥 <strong>Skills
---
<br>

[![My Skills](https://skillicons.dev/icons?i=python,django,mysql,nginx,git,github,githubactions,aws,aws_s3)](https://skillicons.dev)

<br>

Ohters : <br>
- Django-Rest-Framework (DRF)
- Simplejwt (DRF)
- Gunicorn (Middleware)
- AWS EC2
- AWS S3
- AWS RDS
- Pytest
- Code Climate

## <a href="https://github.com/melonmarket#architecture"> Show all the architecture (click) </a>
<br>
<br>


## 📌 <strong>ERD</strong>
---
<br>
 <img width="898" alt="스크린샷 2022-12-14 오후 4 43 16" src="https://user-images.githubusercontent.com/94242504/207535669-16dbd499-02be-4475-9cb8-76e4de0b2e9c.png">

<br>
<br>


## 🗿 <strong>Role</strong>
---
 - **기본 Api 기능 구현**
    - 회원가입 및 로그인 : DRF와 Simplejwt를 이용한 회원 관리
    - 이메일 중복 체크 : 이메일 사전 중복 확인 기능
    - 게시글 CRUD : 게시글 작성, 확인, 수정, 삭제 기능
    - 메인 페이지 확인 : 요청 시 최근 게시글 5개씩 Pagination 적용하여 응답
    - 상세 페이지 확인: 상세 페이지 내용과 함께 글쓴이의 최근 4개 까지의 게시물을 함께 응답
    - 좋아요 기능 : 사용자가 상세 페이지 내에서 좋아요 및 해제가 가능한 기능 (메인 페이지에서 좋아요 수 확인 가능)
    - 조회수 기능 : 상세 페이지를 읽은 조회수를 메인페이지 또는 상세페이지에서 확인 (쿠키를 이용하여 5시간 내 중복 조회 제외)
    - 카테고리 기능 : 카테고리별 최근 게시물 확인 기능
    - 검색 기능 : 제목 기준의 검색 기능

<br>

 - **AWS Setup**
    - AWS S3 : 유저 프로필 사진과 게시글 사진을 AWS S3에 연결하여 업로드
    - AWS RDS : Mysql Database setup 후 Django(WAS)와 연결하여 사용
    - AWS EC2 : Django, gunicorn 및 nginx setup 후 배포

<br>

 - **CI/CD**
    - Pytest, Coverage : Unit 단위의 Test Code 작성 후 Coverage 확인
    - Github Actions (CI) : develop branch에 Pull-Request시 Test Code 및 Coverage 테스트
    - Github Actions (CD) : S3 및 Code Deploy를 통해 Build된 서버 배포

<br>
<br>

## 🛠 <strong>Trouble Shoot</strong>

<br>

### <strong> 1. 로그인 시 Authenticated가 필요없도록 설정하였으나 Headers의 Authorization 부분이 존재하면 항상 403 Forbidden 에러가 발생 </strong>

<br>
해결 : Default Class로 IsAuthenticated를 해지하여도 같은 에러가 발생하였고 해당 에러는 Sign-in View에서 Authentication_classes를 빈 리스트로 override하여 해결
<br>

<img width="380" alt="스크린샷 2022-12-14 오전 2 16 22" src="https://user-images.githubusercontent.com/94242504/207400052-3af43bfe-b428-4205-8e7d-cb47e48b9817.png">


<br>
<br>

### <strong> 2. 게시글 작성/수정 시 Serializer에 SerializedMethod를 이용하여 파일을 개별 분리 후 저장하였으나 이미지 파일이 없거나 잘못된 형식이라도 Null 값으로 저장되는 에러가 발생</strong>

<br>
<div align='center'>
<img width="634" alt="스크린샷 2022-12-15 오후 2 25 42" src="https://user-images.githubusercontent.com/94242504/207779670-4b9cac0d-0b5b-48f6-ad01-94cd0afe9827.png">
</div>
<br>
해결 : ImageSerializer 단계에서 이미지파일을 우선적으로 받은 다음 이미지가 없으면 ValidationError을 발생하도록 수정

<div align='center'>
<img width="671" alt="스크린샷 2022-12-15 오후 2 33 33" src="https://user-images.githubusercontent.com/94242504/207780607-2425c07d-4122-4c61-aefe-bb92309bbd8b.png">
</div>

<br>
<br>

### <strong>3. Pytest로 Test Code 작성할 떄 dummy 게시글 작성 중 Image에서 Content-Type 에러 또는 Encoding 에러 발생</strong>

<br>
해결 : <br> 
1. 전송할 이미지를 불러올 때 django의 SimpleUploadedFile을 이용하여 이미지를 읽어와서 Encoder로 이미지 전달
<br>
2. Multipart/form-data 형식으로 Encoding하기 위하여 requests_toolbelt의 MultipartEncoder를 이용하여 Encoding 후 데이터를 post Method로 전달
<br>

<div align='center'>
<img width="433" alt="스크린샷 2022-12-15 오후 5 24 11" src="https://user-images.githubusercontent.com/94242504/207809370-32232da5-2db8-43dd-919d-0f8c577dfbaf.png">
</div>

