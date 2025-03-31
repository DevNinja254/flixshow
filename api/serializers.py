from rest_framework import serializers
# from django.contrib.auth.models import User
import jwt
from rest_framework_simplejwt.tokens import AccessToken
from django.conf import settings
from django.utils import timezone
from Members.models import Members
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not Members.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user with this email.")
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate_token(self, value):
        try:
            token = AccessToken(value)
            user_id = token['user_id']
            user = Members.objects.get(id=user_id)
        except Exception as e:
            raise serializers.ValidationError(f"Invalid or expired token: {str(e)}")
        self.context['user'] = user
        return value

    def save(self):
        user = self.context['user']
        user.set_password(self.validated_data['new_password'])
        user.save()