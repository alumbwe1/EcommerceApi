from django.contrib import admin # type: ignore

from . import models

# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.Brand)
admin.site.register(models.DeliveryBoy)
admin.site.register(models.Product)


