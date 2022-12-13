'''
user api's URLs
'''
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import UserSignupView, UserCheckView, UserLoginView

urlpatterns = [
    path("signup", UserSignupView.as_view()),
    path("signup/", UserSignupView.as_view()),
    path("check", UserCheckView.as_view()),
    path("check/", UserCheckView.as_view()),
    path("signin", UserLoginView.as_view()),
    path("signin/", UserLoginView.as_view()),
    path("refresh", TokenRefreshView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("verify/", TokenVerifyView.as_view()),
]
