from django.contrib.auth.models import User
from rest_framework import serializers

from user.models.author_model import Profile
from blog.models.post_model import Post
from user.serializers import AuthorSerializer


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Post
        fields = "__all__"
