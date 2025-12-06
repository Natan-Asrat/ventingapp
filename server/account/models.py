from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from server.utils import get_readable_time_since
# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required!")

        email = self.normalize_email(email).lower()
        
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("Invalid email address!")

        if not username:
            raise ValueError("Username is required!")

        username = username.lower()

        user = self.model(email=email, username=username, **extra_fields)
        if password:
            user.set_password(password)
        
        user.save(using=self._db)
        return user
        

        
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length = 255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    connects = models.PositiveIntegerField(default=0)
    connections = models.PositiveIntegerField(default=0)
    connection_requests = models.PositiveIntegerField(default=0)
    email_verified = models.BooleanField(default=False)
    otp_secret = models.CharField(max_length=32, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    post_likes = models.IntegerField(default=0)
    connects_needed_for_connection = models.PositiveIntegerField(default=1)
    last_month_free_connects_date = models.DateTimeField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True) 

    USERNAME_FIELD="email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    @property
    def formatted_date_joined(self):
        return self.date_joined.strftime("%B %d, %Y")


    @property
    def date_joined_since(self):
        return get_readable_time_since(self.date_joined)


class Connection(models.Model):
    initiating_user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='connections_list')
    connected_user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='connected_users')

    reported = models.BooleanField(default=False)
    removed = models.BooleanField(default=False)
    banned = models.BooleanField(default=False)
    connectSpent = models.IntegerField(default=0)

    message = models.CharField(max_length=255, blank=True, null=True)
    reconnection_requested = models.BooleanField(default=False)
    reconnection_count = models.IntegerField(default=0)
    reconnection_requested_by = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='reconnection_requests', blank=True, null=True)
    reconnection_rejected = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    @property
    def formatted_created_at(self):
        return get_readable_time_since(self.created_at)

    @property
    def formatted_updated_at(self):
        return get_readable_time_since(self.updated_at)