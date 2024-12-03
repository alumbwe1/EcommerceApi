from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



# Category model
class Category(models.Model):
    title = models.CharField(max_length=255,unique=True)
    imageUrl = models.URLField(blank=False)
    

    def __str__(self):
        return self.title
    
class Brand(models.Model):
    title = models.CharField(max_length=255,unique=True)
    imageUrl = models.URLField(blank=False)
 

    def __str__(self):
        return self.title

# Product model
class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_featured = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    sizes = models.JSONField() 
    colors = models.JSONField()
    clothesType = models.CharField(max_length=255, default='Unisex')
    imageUrls = models.JSONField(blank=True)# Added image field
    created_at = models.DateTimeField(default=timezone.now,blank=False)
    updated_at = models.DateTimeField(default=timezone.now,blank=False)
    rating = models.FloatField(default=0,blank=False)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,related_name='products')

    def __str__(self):
        return self.title

    def get_like_count(self):
        """Return the count of likes for this product."""
        return self.reactions.filter(user=self.user, product=self).count()

# ProductReaction model for likes and dislikes

