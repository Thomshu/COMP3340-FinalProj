from django.db import models
from django.conf import settings

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    
    def __str__(self): #this is to just help with the Appearance of the names in Django administration aka http://127.0.0.1:8000/admin/item/category/
        return self.name


class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='item_images')
    is_sold = models.BooleanField(default=False) 
    stock = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='items', on_delete=models.CASCADE) # <= if the user is deleted, all the items are deleted as well
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # If stock is 0, set is_sold to True
        if self.stock == 0:
            self.is_sold = True

        else:
            self.is_sold = False
        super().save(*args, **kwargs)


    def __str__(self): 
        return self.name