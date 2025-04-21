from django.db import models
import uuid
from django.contrib.auth.models import User




class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    initiatedAt = models.DateTimeField()
    completedAt = models.DateTimeField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    bearer = models.CharField(max_length=20)
    currency = models.CharField(max_length=3)
    reference = models.CharField(max_length=255)
    lencoReference = models.CharField(max_length=255)
    type = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    source = models.CharField(max_length=20)
    reasonForFailure = models.TextField(null=True, blank=True)
    settlementStatus = models.CharField(max_length=20)
    settlement = models.OneToOneField('Settlement', on_delete=models.CASCADE, null=True, blank=True, related_name='transaction')
    mobileMoneyDetails = models.OneToOneField('MobileMoneyDetails', on_delete=models.CASCADE, null=True, blank=True, related_name='transaction')
    bankAccountDetails = models.OneToOneField('BankAccountDetails', on_delete=models.CASCADE, null=True, blank=True, related_name='transaction')
    cardDetails = models.OneToOneField('CardDetails', on_delete=models.CASCADE, null=True, blank=True, related_name='transaction')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='transactions')

    def __str__(self):
        return f"{self.type} - {self.reference} ({self.status})"

class Settlement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amountSettled = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    createdAt = models.DateTimeField()
    settledAt = models.DateTimeField()
    status = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    accountId = models.CharField(max_length=255)

    def __str__(self):
        return f"Settlement {self.id} - {self.amountSettled} {self.currency} ({self.status})"

class MobileMoneyDetails(models.Model):
    country = models.CharField(max_length=2)
    phone = models.CharField(max_length=20)
    operator = models.CharField(max_length=50)
    accountName = models.CharField(max_length=255)

    def __str__(self):
        return f"Mobile Money: {self.phone} ({self.operator})"

class BankAccountDetails(models.Model):
    # Add fields relevant to bank account details if they appear in other responses
    # For example:
    # bankName = models.CharField(max_length=100, null=True, blank=True)
    # accountNumber = models.CharField(max_length=50, null=True, blank=True)
    # accountHolderName = models.CharField(max_length=255, null=True, blank=True)
    pass

    def __str__(self):
        return "Bank Account Details"

class CardDetails(models.Model):
    # Add fields relevant to card details if they appear in other responses
    # For example:
    # cardNumber = models.CharField(max_length=20, null=True, blank=True)
    # expiryMonth = models.CharField(max_length=2, null=True, blank=True)
    # expiryYear = models.CharField(max_length=4, null=True, blank=True)
    # cardType = models.CharField(max_length=50, null=True, blank=True)
    pass

    def __str__(self):
        return "Card Details"
