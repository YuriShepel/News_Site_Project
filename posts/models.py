from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    body = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)

    published_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)

    status = models.CharField(choices=Status.choices, default=Status.DRAFT, max_length=20)

    tags = TaggableManager()

    rating = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_date']
        indexes = [models.Index(fields=['-published_date'])]

    def __str__(self):
        return self.title
