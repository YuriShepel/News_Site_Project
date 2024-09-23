from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.db.models import Count, Q
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.contrib.postgres.search import SearchVector
from django.views.generic import ListView
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


class PostSearchView(ListView):
    model = Post
    template_name = 'posts/post/search_results.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            return Post.published.filter(
                Q(title__icontains=query) | Q(body__icontains=query)
            ).distinct()
        return Post.published.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')
        return context

# def post_search(request):
#     form = SearchForm()
#     query = None
#     results = []
#
#     if 'query' in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             results = Post.published.annotate(search=SearchVector('title', 'body'), ).filter(search=query)
#     return render(request,
#                   'posts/post/search.html',
#                   {'form': form,
#                    'query': query,
#                    'results': results})
