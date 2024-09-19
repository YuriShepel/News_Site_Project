

from django.shortcuts import render

from django.shortcuts import get_object_or_404

from taggit.models import Tag
from .models import Post



def post_list(request, tag_slug=None):
    posts = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    return render(request, 'posts/post/list.html', {'posts': posts, 'tag': tag})


def post_detail(request, post):
    post = get_object_or_404(Post, slug=post, status=Post.Status.PUBLISHED)
    return render(request, 'posts/post/detail.html', {'post': post})

