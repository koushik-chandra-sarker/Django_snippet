from django.contrib.auth.models import User
from rest_framework import serializers

from author.models.user_model import Profile
from blog.models.post_model import Post
from author.serializers import AuthorSerializer


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Post
        fields = "__all__"
