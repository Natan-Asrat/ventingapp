from django.contrib import admin
from post.models import Like, Post, PostView

# Register your models here.
admin.site.register(Post)
admin.site.register(PostView)
admin.site.register(Like)