from .views import PostingView
from django.urls import path

urlpatterns = [
    path('', PostingView.as_view()),
    #path('<int:pk>/', PostingView.as_view()),
]