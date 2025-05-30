# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from djoser.views import UserViewSet

class CustomUserViewSet(UserViewSet):
    @action(["delete"], detail=False)
    def me(self, request, *args, **kwargs):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)