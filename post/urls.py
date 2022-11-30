from .views import PostCreateView, PostListViewset,PostCategoryView, PostDetailView, PostLikeView
from django.urls import path, include, re_path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'list', PostListViewset, basename= '')

urlpatterns = [
    path('', PostCreateView.as_view()),
    path('', include(router.urls)),
    re_path('^(?P<category>.+)/', PostCategoryView.as_view()),
    path('<int:pk>/', PostDetailView.as_view()),
    path('<int:pk>/heart/', PostLikeView.as_view()),
]