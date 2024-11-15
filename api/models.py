from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.utils import timezone

class User(AbstractUser):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, unique=True)
    username = models.CharField(max_length=100, unique=True)
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )
    
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.ManyToManyField('Tag', related_name="posts")
    created_at = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=False)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(default=timezone.now)

