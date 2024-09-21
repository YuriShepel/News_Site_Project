from django.urls import path
from . import views

from .views import post_comment

app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<slug:post>/', views.post_detail, name='post_detail'),
    # Изменяем регулярное выражение для tag_slug, чтобы поддерживать кириллицу
    path('tag/<str:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),

]
