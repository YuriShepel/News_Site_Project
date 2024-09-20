from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.db.models import Count, Q

from taggit.models import Tag
from .models import Post, Comment
from .forms import CommentForm


def post_list(request, tag_slug=None):
    posts = Post.published.annotate(total_comments=Count(
        'comments',
        filter=Q(comments__active=True)))

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,
                                slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    return render(request,
                  'posts/post/list.html',
                  {'posts': posts, 'tag': tag})


def post_detail(request, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(request,
                  'posts/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request,
                  'posts/post/comment.html',
                  {'post': post,
                   'form': form,
                   'comment': comment})
