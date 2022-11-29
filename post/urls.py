from .views import PostCreateView, PostListViewset, PostDetailView, PostLikeView
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'list', PostListViewset, basename= '')

urlpatterns = [
    path('', PostCreateView.as_view()),
    path('', include(router.urls)),
    path('<int:pk>/', PostDetailView.as_view()),
    path('<int:pk>/heart/', PostLikeView.as_view()),
]