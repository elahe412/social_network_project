from django.contrib import admin

# Register your models here.
from apps.post.models import Comment, Like, Post

admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Post)
