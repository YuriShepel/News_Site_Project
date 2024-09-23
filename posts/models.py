from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from taggit.managers import TaggableManager
from .utils import time_since_published, get_short_body
from django.urls import reverse
from .utils import custom_slugify


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset() \
            .filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique_for_date='published_date')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')

    body = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)

    published_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)

    status = models.CharField(choices=Status.choices, default=Status.DRAFT, max_length=20)

    tags = TaggableManager()

    votes_up_count = models.PositiveIntegerField(default=0)
    votes_down_count = models.PositiveIntegerField(default=0)
    rating = models.IntegerField(default=0)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-created_date']
        indexes = [models.Index(fields=['-published_date'])]

    def __str__(self):
        return self.title

    def time_since_published(self):
        return time_since_published(self.published_date)

    def get_short_body(self, length=800):
        return get_short_body(self.body, length)

    def get_absolute_url(self):
        return reverse('posts:post_detail',
                       args=[self.slug])

    def save(self, *args, **kwargs):
        # Если пост новый и слаг не установлен, создаём слаг
        if not self.slug:
            self.slug = custom_slugify(self.title)
        # Сохраняем пост с тегами
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=200)
    body = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_date']
        indexes = [models.Index(fields=['-created_date'])]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'



    def time_since_published(self):
        return time_since_published(self.created_date)
