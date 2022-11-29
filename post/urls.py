from .views import PostCreateView, PostDetailView, PostLikeView
from django.urls import path

urlpatterns = [
    path('', PostCreateView.as_view()),
    path('<int:pk>/', PostDetailView.as_view()),
    path('<int:pk>/heart/', PostLikeView.as_view()),
]