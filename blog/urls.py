
from django.urls import path, include
from rest_framework import routers, urlpatterns
from blog.views import PostApi, index, PostListApi, SinglePostApi

router = routers.DefaultRouter()
router.register('posts', PostApi, basename='post')



urlpatterns = [
    path('', include(router.urls)),
    path('allPosts/', PostListApi.as_view()),
    path('post/<int:pk>/', SinglePostApi.as_view())
]
