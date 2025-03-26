from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from posts import models

class StoreCategory(models.Model):
    """Model for store categories like Electronics, Clothing, etc."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='store_categories/', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Store Categories"

class Store(models.Model):
    """Model for individual stores."""
    STORE_STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('closed', 'Closed'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_stores')
    name = models.CharField(max_length=200)
    category = models.ForeignKey(StoreCategory, on_delete=models.PROTECT, related_name='stores')
    description = models.TextField()
    logo = models.ImageField(upload_to='store_logos/')
    banner = models.ImageField(upload_to='store_banners/', blank=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    
    # Operating hours
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    business_days = models.CharField(max_length=100, help_text="e.g., Mon-Sat")
    
    # Store metrics
    rating = models.FloatField(default=0.0)
    total_reviews = models.IntegerField(default=0)
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Status and timestamps
    status = models.CharField(max_length=20, choices=STORE_STATUS_CHOICES, default='pending')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class StoreProduct(models.Model):
    """Model for products specific to a store."""
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='store_products/')
    category = models.CharField(max_length=100)  # Product category within the store
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.store.name}"

class StoreReview(models.Model):
    """Model for store reviews."""
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('store', 'user')  # One review per user per store

    def __str__(self):
        return f"{self.user.username}'s review for {self.store.name}"

class StoreProductCategory(models.Model):
    title = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='stores_category_images/', blank=True, null=True)  # optional

    def __str__(self):
        return self.title

class StoreProduct(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(StoreProductCategory, on_delete=models.SET_NULL, null=True, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.store.name}"

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} - {self.store.name}"
