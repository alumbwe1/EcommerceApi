from rest_framework import serializers
from .models import PhoneOTP
from extras.models import Address

class PhoneOTPSerializer(serializers.ModelSerializer):
    """
    Basic serializer for inspecting PhoneOTP objects.
    """
    class Meta:
        model = PhoneOTP
        fields = ['id', 'address', 'otp', 'created_at', 'is_verified']


class GenerateOTPSerializer(serializers.Serializer):
    """
    Input: phone → returns or creates a PhoneOTP and sends a fresh OTP.
    """
    phone = serializers.CharField(write_only=True)

    def create(self, validated_data):
        phone = validated_data['phone']
        try:
            address = Address.objects.get(phone=phone)
        except Address.DoesNotExist:
            raise serializers.ValidationError("Phone not found")
        phone_otp, _ = PhoneOTP.objects.get_or_create(address=address)
        phone_otp.generate_otp()
        return phone_otp


class VerifyOTPSerializer(serializers.Serializer):
    """
    Input: phone + otp → validates and marks is_verified=True.
    """
    phone = serializers.CharField(write_only=True)
    otp = serializers.CharField(max_length=6)

    def validate(self, attrs):
        phone = attrs['phone']
        try:
            address = Address.objects.get(phone=phone)
        except Address.DoesNotExist:
            raise serializers.ValidationError("Phone not found")
        try:
            otp_obj = PhoneOTP.objects.get(address=address, otp=attrs['otp'])
        except PhoneOTP.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP")
        attrs['otp_obj'] = otp_obj
        return attrs

    def save(self):
        otp_obj = self.validated_data['otp_obj']
        otp_obj.is_verified = True
        otp_obj.save()
        return otp_obj