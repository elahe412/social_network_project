from django.contrib import admin

from apps.post.models import Comment, Like, Post


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    fields = ['id', 'post', 'user', 'body', 'created']
    list_display = ['id', 'post', 'user', 'created']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    model = Like
    fields = ['id', 'post', 'user', 'value', 'created']
    list_display = ['id', 'post', 'user', 'value', 'created']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post
    fields = ['id', 'post', 'author', 'content', 'image', 'created']
    list_display = ['id', 'author', 'created']

