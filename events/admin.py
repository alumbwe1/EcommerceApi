from django.contrib import admin
from .models import Event, Ticket, TicketType, Category
# Register your models here.
admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(TicketType)
admin.site.register(Category)
