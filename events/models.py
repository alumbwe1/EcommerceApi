# models.py
from django.db import models
from django.contrib.auth.models import User
from io import BytesIO
from django.core.files import File
import uuid
import qrcode
from cloudinary.models import CloudinaryField

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Event(models.Model):
    host = models.ForeignKey(User, related_name="events", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = CloudinaryField('event_images', blank=False) 
    location = models.CharField(max_length=255)
    date = models.DateTimeField()
    
    phone_number = models.CharField(max_length=20)
    TICKET_TYPE_CHOICES = [
        ('free', 'Free'),
        ('paid', 'Paid'),
    ]

    ticket_type = models.CharField(max_length=10, choices=TICKET_TYPE_CHOICES)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.host.username}"

class TicketType(models.Model):
    event = models.ForeignKey(Event, related_name="ticket_types", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity_available = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.event.title}"

class Ticket(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('mobile_money', 'Mobile Money'),
        ('cash', 'Cash'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name="tickets", on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    ticket_number = models.CharField(max_length=100, unique=True, blank=True)
    qr_code = CloudinaryField('qr_codes/', blank=True, null=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.ticket_type.name} - {self.event.title}"

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = f"{self.event.id}-{self.user.id}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)
        self.generate_qr_code()

    def generate_qr_code(self):
        data = f"Ticket: {self.ticket_number}\nEvent: {self.event.title}\nType: {self.ticket_type.name}\nUser: {self.user.username}"
        qr = qrcode.make(data)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        buffer.seek(0)
        filename = f"{self.ticket_number}.png"
        self.qr_code.save(filename, File(buffer), save=False)
        super().save(update_fields=['qr_code'])