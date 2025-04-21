from rest_framework import serializers
from .models import Transaction, Settlement, MobileMoneyDetails, BankAccountDetails, CardDetails

class SettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        fields = '__all__'

class MobileMoneyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileMoneyDetails
        fields = '__all__'

class BankAccountDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccountDetails
        fields = '__all__'

class CardDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardDetails
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    settlement = SettlementSerializer(read_only=True)
    mobileMoneyDetails = MobileMoneyDetailsSerializer(read_only=True)
    bankAccountDetails = BankAccountDetailsSerializer(read_only=True)
    cardDetails = CardDetailsSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'

    def create(self, validated_data):
        settlement_data = validated_data.pop('settlement', None)
        mobile_money_data = validated_data.pop('mobileMoneyDetails', None)
        bank_account_data = validated_data.pop('bankAccountDetails', None)
        card_data = validated_data.pop('cardDetails', None)

        transaction = Transaction.objects.create(**validated_data)

        if settlement_data:
            Settlement.objects.create(transaction=transaction, **settlement_data)
        if mobile_money_data:
            MobileMoneyDetails.objects.create(transaction=transaction, **mobile_money_data)
        if bank_account_data:
            BankAccountDetails.objects.create(transaction=transaction, **bank_account_data)
        if card_data:
            CardDetails.objects.create(transaction=transaction, **card_data)

        return transaction

    def update(self, instance, validated_data):
        settlement_data = validated_data.pop('settlement', None)
        mobile_money_data = validated_data.pop('mobileMoneyDetails', None)
        bank_account_data = validated_data.pop('bankAccountDetails', None)
        card_data = validated_data.pop('cardDetails', None)

        # Update Transaction fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update or create related models
        if settlement_data:
            settlement, created = Settlement.objects.update_or_create(transaction=instance, defaults=settlement_data)
        if mobile_money_data:
            mobile_money, created = MobileMoneyDetails.objects.update_or_create(transaction=instance, defaults=mobile_money_data)
        if bank_account_data:
            bank_account, created = BankAccountDetails.objects.update_or_create(transaction=instance, defaults=bank_account_data)
        if card_data:
            card, created = CardDetails.objects.update_or_create(transaction=instance, defaults=card_data)

        return instance
