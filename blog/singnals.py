from django.db.models.signals import post_save

from blog.Utility import unique_slug_generator
from blog.models import Post


def blog_slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        instance.save()


def category_slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        instance.save()


post_save.connect(blog_slug_generator, sender=Post)
post_save.connect(category_slug_generator, sender=Post)
