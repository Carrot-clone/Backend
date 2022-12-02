from django.urls import path
from .views import UserSignupView, UserCheckView, UserLoginView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('signup',UserSignupView.as_view()),
    path('signup/',UserSignupView.as_view()),
    path('check',UserCheckView.as_view()),
    path('check/',UserCheckView.as_view()),
    path('login',UserLoginView.as_view()),
    path('login/',UserLoginView.as_view()),
    path('refresh',TokenRefreshView.as_view()),
    path('refresh/',TokenRefreshView.as_view()),
    path('verify/', TokenVerifyView.as_view()),
]