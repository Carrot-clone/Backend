from django.urls import path
from .views import UserSignupView, UserCheckView, UserLoginView

urlpatterns = [
    path('signup/',UserSignupView.as_view()),
    path('check/',UserCheckView.as_view()),
    path('login/',UserLoginView.as_view()),
]