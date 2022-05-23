import string
import random

from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.utils.text import slugify

from django.contrib.auth.models import User

from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager

from App_Project.settings import AUTH_USER_MODEL
from blog.models.category_model import Category

STATUS_CHOICES = (
    ("DRAFTED", 'Draft'),
    ("PUBLISHED", 'Publish'),
)


class Post(models.Model):
    title = models.CharField(max_length=100, null=False)
    image = models.ImageField(default='article-default.jpg',
                              upload_to='post_images')
    content = RichTextUploadingField(blank=True)
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='articles')
    publish_date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True, editable=False)
    tags = TaggableManager(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='DRAFT')

    def save(self, *args, **kwargs):
        if not self.slug:
            generated_slug = slugify(self.title)
            while Post.objects.filter(slug=generated_slug).exists():
                # Generate a random alphanumeric string of length 6
                random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                generated_slug = slugify(self.title + ' ' + random_string)
            self.slug = generated_slug
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:posts',
                       kwargs={'slug': self.slug})
