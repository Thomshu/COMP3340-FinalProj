from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    # Add your custom fields here
    is_admin = models.BooleanField(default=False)
    is_inventoryManager = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

class Profile(models.Model):
    staff = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to='Profile_Images', null=True, blank=True) #uses default image if none is applied

    def __str__(self):
        return f'{self.staff.username}-Profile'
    
