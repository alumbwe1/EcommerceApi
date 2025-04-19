from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Address(models.Model):
    HOME = "home"
    OFFICE = "office"
    SCHOOL = "school"
    ADDRESSTYPES = (
        (HOME, "Home"),
        (OFFICE, "Office"),
        (SCHOOL, "School"),
    )
    lat = models.FloatField(null=True, blank=True)
    log = models.FloatField(null=True, blank=True)
    isDefault = models.BooleanField(default=False)
    room_number = models.CharField(max_length=50, blank=True, null=True)
    apartment = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField( max_length=255, blank=False)
    phone = models.CharField( max_length=255, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    addressType = models.CharField(choices=ADDRESSTYPES, max_length=10, default=HOME)


    def __str__(self):

        return "{}/{}".format(self.user.username, self.addressType, self.phone)
    

class Extras(models.Model):
    image = models.ImageField(upload_to='extras/', blank=True, null=True)
    isVerified = models.BooleanField(default=False)
    otp =models.CharField(default='', max_length=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{}/{}".format(self.user.username, self.id)

    def __str__(self):
        return "{}/{}".format(self.user.username, self.id)
    