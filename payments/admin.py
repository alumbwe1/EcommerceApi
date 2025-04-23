from django.contrib import admin
from payments import models

# Register your models here.
admin.site.register(models.BankAccountDetails)
admin.site.register(models.CardDetails)
admin.site.register(models.Settlement)
admin.site.register(models.MobileMoneyDetails)
admin.site.register(models.Transaction)
