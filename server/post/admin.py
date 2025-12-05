from django.contrib import admin
from post.models import ClusterMember, Like, Post, PostView, PreviousRecommendedPost, UserInterest

# Register your models here.
admin.site.register(Post)
admin.site.register(PostView)
admin.site.register(Like)
admin.site.register(UserInterest)
admin.site.register(PreviousRecommendedPost)
admin.site.register(ClusterMember)