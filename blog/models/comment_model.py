from django.contrib.auth.models import User
from django.db import models

from django.utils import timezone

from blog.models.post_model import Post


class Comment(models.Model):
    blog = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_date = models.DateTimeField(default=timezone.now)
    content = models.TextField()