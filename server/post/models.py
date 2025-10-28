from django.db import models
import uuid
from server.utils import get_readable_time_since
# Create your models here.
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    posted_by = models.ForeignKey('account.User', on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='post_images', null=True, blank=True) # keep it as one image per post
    archived = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    saves = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def formatted_created_at(self):
        return get_readable_time_since(self.created_at)

    @property
    def formatted_updated_at(self):
        return get_readable_time_since(self.updated_at)

class Like(models.Model):
    post = models.ForeignKey('post.Post', on_delete=models.CASCADE, related_name='likes_list')
    liked_by = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='liked_posts')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def formatted_created_at(self):
        return get_readable_time_since(self.created_at)

    @property
    def formatted_updated_at(self):
        return get_readable_time_since(self.updated_at)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey('post.Post', on_delete=models.CASCADE, related_name='comments_list')
    commented_by = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='commented_posts')
    message = models.CharField(max_length=1000)
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies_list')
    archived = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    replies = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def formatted_created_at(self):
        return get_readable_time_since(self.created_at)

    @property
    def formatted_updated_at(self):
        return get_readable_time_since(self.updated_at)

class Save(models.Model):
    post = models.ForeignKey('post.Post', on_delete=models.CASCADE, related_name='saved_list')
    saved_by = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='saved_posts')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def formatted_created_at(self):
        return get_readable_time_since(self.created_at)

    @property
    def formatted_updated_at(self):
        return get_readable_time_since(self.updated_at)

class LikeComment(models.Model):
    comment = models.ForeignKey('post.Comment', on_delete=models.CASCADE, related_name='comment_likes_list')
    liked_by = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='liked_comments')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def formatted_created_at(self):
        return get_readable_time_since(self.created_at)

    @property
    def formatted_updated_at(self):
        return get_readable_time_since(self.updated_at)

class PaymentInfo(models.Model):
    post = models.ForeignKey('post.Post', on_delete=models.CASCADE, related_name='payment_info_list')
    method = models.CharField(max_length=255)
    account = models.CharField(max_length=255)
    nameOnAccount = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def formatted_created_at(self):
        return get_readable_time_since(self.created_at)

    @property
    def formatted_updated_at(self):
        return get_readable_time_since(self.updated_at)