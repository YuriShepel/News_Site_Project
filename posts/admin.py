from django.contrib import admin
from posts.models import Post, Comment, CustomUser
from django.contrib.auth.admin import UserAdmin


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'published_date', 'status', 'rating']
    list_filter = ['status', 'created_date', 'published_date', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'published_date'
    ordering = ['status', 'published_date']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'created_date', 'active']
    list_filter = ['active', 'created_date', 'updated_date']
    search_fields = ['name', 'body']


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_staff', 'is_active', 'rating', 'last_login']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'avatar', 'rating', 'votes_up_count', 'votes_down_count', 'comments_count')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

