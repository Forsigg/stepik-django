from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'post', 'text', 'created_at')
    list_filter = ('username', 'created_at')
    search_fields = ('username', 'text')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)