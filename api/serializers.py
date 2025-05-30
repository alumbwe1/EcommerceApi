
from django.contrib.auth import get_user_model

User = get_user_model()

class UserDeleteSerializer(serializers.Serializer):
    def validate(self, attrs):

        return attrs

    def delete_user(self):
        user = self.context['request'].user
        user.delete()
