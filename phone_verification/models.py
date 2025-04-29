from django.db import models
from extras.models import Address
import random



class PhoneOTP(models.Model):
    address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='otp')
    otp = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.save()
        return self.otp

    def __str__(self):
        return f"{self.address.phone} - {self.otp}"
