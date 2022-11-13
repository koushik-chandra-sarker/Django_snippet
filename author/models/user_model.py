import hashlib
from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from App_Project.utils import send_mail, send_html_mail
from author.models.role_model import Role


class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not username:
            raise ValueError("User must have an username")
        email = email.lower()
        username = username.title()
        first_name = first_name.title()
        last_name = last_name.title()

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name

        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, first_name, last_name, password=None):
        user = self.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    roles = models.ManyToManyField(Role, blank=True)
    email = models.EmailField(max_length=200, unique=True, verbose_name='email')
    username = models.CharField(max_length=200, unique=True, verbose_name='username', null=False, blank=False)
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name')

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.email

    # def has_perm(self, perm, obj=None):
    #     return self.is_superuser
    #
    # def has_module_perms(self, app_label):
    #     return self.is_superuser

    class Meta:
        verbose_name_plural = 'Users'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='profile-pic-default.jpg', upload_to='profile_images')
    cover_pic = models.ImageField(default='cover-pic-default.jpg', upload_to='cover_images')
    bio = models.CharField(max_length=100,
                           help_text="Short Bio (eg. I love traveling and games)")

    address = models.CharField(max_length=100,
                               help_text="Enter Your Address"
                               )

    city = models.CharField(max_length=100, help_text="Enter Your City")

    country = models.CharField(max_length=100, help_text="Enter Your Country")

    zip_code = models.CharField(max_length=100, help_text="Enter Your Zip Code")

    twitter_url = models.CharField(max_length=250,
                                   default="#",
                                   blank=True, null=True,
                                   help_text="Enter # if you don't have an account")
    instagram_url = models.CharField(max_length=250,
                                     default="#",
                                     blank=True, null=True,
                                     help_text=
                                     "Enter # if you don't have an account")
    facebook_url = models.CharField(max_length=250, default="#",
                                    blank=True, null=True,
                                    help_text=
                                    "Enter # if you don't have an account")
    github_url = models.CharField(max_length=250, default="#",
                                  blank=True, null=True,
                                  help_text=
                                  "Enter # if you don't have an account")

    email_confirmed = models.BooleanField(default=False)

    created_on = models.DateTimeField(default=timezone.now)

    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s Profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    if not created:
        if not Profile.objects.filter(user=instance).exists():
            Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class EmailConfirmed(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=500)
    email_confirm = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = 'User Email Confirm'


@receiver(post_save, sender=User)
def create_user_email_confirmation(sender, instance, created, **kwargs):
    if created:
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        email_confirm_instance = EmailConfirmed(user=instance)
        user_encoded = f'{instance.email}-{dt}'.encode()
        activation_key = hashlib.sha224(user_encoded).hexdigest()
        email_confirm_instance.activation_key = activation_key
        email_confirm_instance.save()
        send_html_mail(instance.email, "/author/verify-mail/?token=" + activation_key, "test url", "Confirm Email")
