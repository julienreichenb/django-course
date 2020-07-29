from django.contrib import admin
from django.forms import Textarea
from django.db import models
from blog.models import PostCategory, Post, Comment


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'published',
        'created_at',
        'comments_count',
    )
    list_filter = ['category', 'published']
    autocomplete_fields = ['category']
    search_fields = ['title']
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 30, 'cols': 190})}
    }

    def comments_count(self, obj):
        return Comment.objects.filter(post=obj).count()
    comments_count.short_description = 'Comments'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    autocomplete_fields = ['post']
    list_display = ('post'[:20], 'author', 'status', 'moderation_text'[:20], 'text'[:20], )
    list_editable = ['status', 'moderation_text']
    list_filter = ['status']
    search_fields = ['post__title', 'author']
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 190})}
    }
