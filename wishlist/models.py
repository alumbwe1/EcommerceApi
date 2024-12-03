from django.db import models
from django.contrib.auth.models import User # type: ignore
from posts.models import Product

# Create your models here.
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_reactions')  # ForeignKey to the User model
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reactions')  # ForeignKey to the Product model

    class Meta:
        unique_together = ('user', 'product')  # Ensure a user can only react once per product

    def __str__(self):
        return f"{self.user.username} reacted to {self.product.title}"