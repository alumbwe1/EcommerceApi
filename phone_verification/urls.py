from django.urls import path
from .views import GeneratePhoneOTP, VerifyPhoneOTP

urlpatterns = [
    path('generate/', GeneratePhoneOTP.as_view(), name='otp-generate'),
    path('verify/',   VerifyPhoneOTP.as_view(),   name='otp-verify'),
]