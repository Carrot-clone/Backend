from django.urls import path, include, re_path
from rest_framework import routers
from .views import (
    PostCreateView,
    PostListViewset,
    PostCategoryView,
    PostDetailView,
    PostLikeView,
    PostImageUpdateView,
)

router = routers.DefaultRouter()
router.register(r"list", PostListViewset, basename="")

urlpatterns = [
    path("", PostCreateView.as_view()),
    path("", include(router.urls)),
    re_path("category/", PostCategoryView.as_view()),
    path("<int:pk>", PostDetailView.as_view()),
    path("<int:pk>/", PostDetailView.as_view()),
    path("<int:pk>/heart", PostLikeView.as_view()),
    path("<int:pk>/heart/", PostLikeView.as_view()),
    path("<int:pk>/<str:img>", PostImageUpdateView.as_view()),
    path("<int:pk>/<str:img>/", PostImageUpdateView.as_view()),
]
