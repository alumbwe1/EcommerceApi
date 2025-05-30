from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Category model

#But for now i stick to the admin making the admin creating the categories not the brands or restraurant

class Category(models.Model):
    #user = models.ForeignKey(User,on_delete=models.CASCADE, default=get_default_user)
    title = models.CharField(max_length=255, unique=True)
    image = CloudinaryField('category_images', blank=False) 
    brands = models.ManyToManyField('Brand', related_name='categories', blank=True) 

    def __str__(self):
        return self.title

def get_default_user():
    return User.objects.first().id if User.objects.exists() else None

#Expected JSON FORMAT
#Addon Model e,g in JSON format: {'Water': 5.00, 'Extra Cheese': 2.50}
class Addon(models.Model):
    name = models.CharField(max_length=255,unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  

    def __str__(self):
        return f"{self.name} - K{self.price}"
    
#Camous model e.g CBU,UNZA well the the brand has to choose the campus they will be working with
class Campus(models.Model):
    name = models.CharField(max_length=255)

# Brand/Restraurant model 
class Brand(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='brands', )  
    title = models.CharField(max_length=255, unique=True)
    image = CloudinaryField('brand_images', blank=False)  
    description = models.TextField(blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True, blank=True)
    rating = models.IntegerField(default=0, blank=True)
    discount = models.IntegerField(default=0, blank=True)
    cuisine_types = models.TextField(blank=True)
    cover_photo = CloudinaryField('brand_covers/', blank=True, null=True)  
    opening_hours = models.CharField(max_length=100, null=True)
    min_delivery_time = models.PositiveIntegerField(help_text="Minimum delivery time in minutes", null=True)  
    max_delivery_time = models.PositiveIntegerField(help_text="Maximum delivery time in minutes", null=True)

    def __str__(self):
        return self.title

# Product model should be associated with
#  the brand,category and the brand can
#  add addons with above json format 
class Product(models.Model):
    title = models.CharField(max_length=100)
    addons = models.ManyToManyField(Addon, blank=True)
    description = models.TextField()
    is_featured = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    imagePublicIds = models.JSONField(default=list)
    
    # List of ingredients used in the dish
    ingredients = models.JSONField(blank=True, null=True)  
    # Dietary restrictions (e.g., vegan, gluten-free)
    dietary_restrictions = models.JSONField(blank=True, null=True)  
    imageUrls = models.JSONField(blank=True,default=list)
    created_at = models.DateTimeField(default=timezone.now, blank=False)
    updated_at = models.DateTimeField(default=timezone.now, blank=False)
    rating = models.FloatField(default=0, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')

    #JSON format: {'Water': 5.00, 'Extra Cheese': 2.50} for addons
    addons = models.JSONField(
        blank=True,
        null=True,
        help_text="JSON format: {'Water': 5.00, 'Extra Cheese': 2.50}"
    )

    def __str__(self):
        return self.title
    


#Delivery partner #[InFuture should be a seperate]
class DeliveryBoy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    nrc_front = CloudinaryField('nrc_pics', blank=True)
    nrc_back = CloudinaryField('nrc_pics', blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    profile_pic = CloudinaryField('delivery_boy_pics', blank=True)
    nrc_number = models.CharField(max_length=255,blank=True)
    vehicle_type = models.CharField(max_length=100, choices=[('bike', 'Bike'), ('car', 'Car'),('walk','Walk')], default='bike')
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return self.name



