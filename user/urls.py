from django.urls import path
from .views import UserSignupView, UserCheckView

urlpatterns = [
    path('signup/',UserSignupView.as_view()),
    path('check/',UserCheckView.as_view()),
]