from django.contrib import admin

# Register your models here.
from App_Project.baseAdmin import CustomAdmin
from blog.models.category_model import Category
from blog.models.comment_model import Comment
from blog.models.like_model import Like
from blog.models.post_model import Post


@admin.register(Post)
class PostAdmin(CustomAdmin):
    list_display = ['title', 'author', 'category', 'publish_date', 'status']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass
