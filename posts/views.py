from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.db.models import Count, Q
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from taggit.models import Tag
from .models import Post
from .forms import CommentForm, SearchForm


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
    comments = post.comments.filter(active=True).order_by('-created_date')
    form = CommentForm()

    return render(request,
                  'posts/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'comment': {
                'id': comment.id,
                'name': comment.name,
                'body': comment.body,
                'created_date': comment.created_date.strftime("%d.%m.%Y в %H:%M")
            }})
        else:
            messages.success(request, 'Комментарий успешно добавлен.')
            return redirect(reverse('posts:post_detail', kwargs={'post': post.slug}))
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors})
        else:
            messages.error(request, 'Ошибка при добавлении комментария. Пожалуйста, проверьте введенные данные.')
            return redirect(reverse('posts:post_detail', kwargs={'post': post.slug}))


def post_search_view(request):
    query = request.GET.get('query', '')
    if query:
        search_query = SearchQuery(query, config='simple')
        posts = Post.published.annotate(
            search=SearchVector('title', 'body', config='simple'),
            rank=SearchRank(SearchVector('title', 'body', config='simple'), search_query)
        ).filter(
            Q(search=search_query)
        ).order_by('-rank')
    else:
        posts = Post.published.none()
    context = {
        'posts': posts,
        'query': query,
    }
    return render(request, 'posts/post/search_results.html', context)
