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


## 🗿 <strong>Role</strong>
---
 - **기본 Api 기능 구현**
    - 회원가입 및 로그인 : DRF와 Simplejwt를 이용한 회원 관리
    - 이메일 중복 체크 : 이메일 사전 중복 확인 기능
    - 게시글 CRUD : 게시글 작성, 확인, 수정, 삭제 기능
    - 메인 페이지 확인 : 요청 시 최근 게시글 5개씩 Pagination 적용하여 응답
    - 상세 페이지 확인: 상세 페이지 내용과 함께 글쓴이의 최근 4개 까지의 게시물을 함께 응답
    - 좋아요 기능 : 사용자가 상세 페이지내에서 좋아요 및 해제가 가능한 기능 (메인 페이지에서 좋아요 수 확인 가능)
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
    - Github Actions (CI) : develop branch에 Pull-Request마다 Test Code 및 Coverage 확인
    - Github Actions (CD) : Elasticbeanstalk 사용 예정

<br>
<br>

## 🛠 <strong>Trouble Shoot</strong>

<br>

### 1. 로그인 시 Authenticated가 필요없도록 설정하였으나 Headers의 Authorization 부분이 존재하면 항상 403 Forbidden 에러가 발생

<img width="380" alt="스크린샷 2022-12-14 오전 2 16 22" src="https://user-images.githubusercontent.com/94242504/207400052-3af43bfe-b428-4205-8e7d-cb47e48b9817.png">

<br>
해결 : Default Class로 IsAuthenticated를 해지하여도 같은 에러가 발생하였고 해당 에러는 Sign-in View에서 Authentication_classes를 빈 리스트로 override하여 해결

