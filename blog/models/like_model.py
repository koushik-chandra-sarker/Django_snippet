from django.contrib.auth.models import User
from django.db import models

from Django_BlogWithPermission.settings import AUTH_USER_MODEL
from blog.models.post_model import Post


class Like(models.Model):
    user_id = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    blog_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField()
