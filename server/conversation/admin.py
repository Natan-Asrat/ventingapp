from django.contrib import admin
from .models import Conversation, Member, Message, Reaction
# Register your models here.
admin.site.register(Conversation)
admin.site.register(Member)
admin.site.register(Message)
admin.site.register(Reaction)