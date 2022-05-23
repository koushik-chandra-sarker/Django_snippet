import datetime

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import generic
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, DjangoObjectPermissions, DjangoModelPermissions

from App_Project.permissions import IsOwner, IsSuperuser, CustomModelPermissions
from blog.models.post_model import Post
from blog.serializers import PostSerializer


def index(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


class PostListApi(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class SinglePostApi(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostApi(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [DjangoModelPermissions ]
