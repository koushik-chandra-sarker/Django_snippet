from django.contrib import admin

# Register your models here.

from blog.models.category_model import Category
from blog.models.comment_model import Comment
from blog.models.like_model import Like
from blog.models.post_model import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_filter = ["category"]


@admin.register(Category)
class BlogAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass
