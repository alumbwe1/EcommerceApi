from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from twilio.rest import Client
import logging

logger = logging.getLogger(__name__)

from .serializers import GenerateOTPSerializer, VerifyOTPSerializer, PhoneOTPSerializer

class GeneratePhoneOTP(APIView):
    def post(self, request):
        logger.debug(f"GeneratePhoneOTP received data: {request.data}")
        serializer = GenerateOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        logger.debug(f"GeneratePhoneOTP validated data: {serializer.validated_data}")
        otp_obj = serializer.save()
        logger.debug(f"Generated OTP {otp_obj.otp} for address {otp_obj.address.id}")

        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=f"Your OTP is {otp_obj.otp}",
                from_=settings.TWILIO_FROM_PHONE,
                to=otp_obj.address.phone
            )
            logger.debug(f"Twilio message sent: SID={message.sid}")
        except Exception as e:
            logger.error(f"Error sending OTP SMS: {e}", exc_info=True)
            return Response({"error": "Failed to send OTP SMS"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = PhoneOTPSerializer(otp_obj).data
        return Response(data, status=status.HTTP_200_OK)

class VerifyPhoneOTP(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True, "message": "Phone verified"}, status=status.HTTP_200_OK)
