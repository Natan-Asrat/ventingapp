from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length = 255)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length = 50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    @property
    def formatted_created_at(self):
        return self.created_at.strftime("%B %d, %Y")
    
    @property
    def formatted_updated_at(self):
        return self.updated_at.strftime("%B %d, %Y")
    
    @property
    def created_since(self):
        return get_readable_time_since(self.created_at)

    @property
    def updated_since(self):
        return get_readable_time_since(self.updated_at)
    
    def __str__(self):
        return self.name