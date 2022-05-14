
from django.urls import path, include
from rest_framework import routers, urlpatterns
from blog.views import PostApi, index, PostListApi

router = routers.DefaultRouter()
router.register('posts', PostApi, basename='post')



urlpatterns = [
    path('', include(router.urls))
    # path('posts/', PostListApi.as_view()),
    # path('posts/<int:pk>/', PostApi.as_view())
]
