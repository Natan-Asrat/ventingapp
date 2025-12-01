from django.db import models

class ConversationCategoryOptions(models.TextChoices):
    PRIMARY = "primary", "Primary"
    SECONDARY = "secondary", "Secondary"
    REQUESTS = "requests", "Requests"
    ARCHIVED = "archived", "Archived"

    

# Create your models here.
class Conversation(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    members_count = models.IntegerField(default=2)
    active = models.BooleanField(default=True)
    logo = models.ImageField(upload_to="conversation_logos/", blank=True, null=True)

    is_group = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or 'No Name'

class Member(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name="memberships")
    category = models.CharField(max_length=255, choices=ConversationCategoryOptions.choices)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.conversation.name}"
    
class Message(models.Model):
    message = models.CharField(max_length=255)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="replies")
    reaction_count = models.IntegerField(default=0)
    reply_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.conversation.name} - {self.message}"


class Reaction(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    reaction = models.CharField(max_length=16)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} reacts to '{self.message.message}' with {self.reaction}"
    
