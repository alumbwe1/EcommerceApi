from enum import unique
from typing_extensions import override
from django.db import models
from django.contrib.auth.models import User # type: ignore
from posts.models import Product, Brand

# Create your models here.
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_reactions')  # ForeignKey to the User model
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reactions')  # ForeignKey to the Product model

    class Meta:
        unique_together = ('user', 'product')  

    def __str__(self):
        return f"{self.user.username} reacted to {self.product.title}"

class BrandWishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='brands_reactions')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='reactions')

    class Meta:
        unique_together = ('user', 'brand')
        
    def __str__(self):
        return f"{self.user.username} reeacted to {self.brand.title}"