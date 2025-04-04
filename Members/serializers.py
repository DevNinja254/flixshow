from .models import *
from rest_framework import serializers
from django.contrib.auth import authenticate
class ErrosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Errors
        fields = "__all__"
class BettingRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BettingRecords
        fields = "__all__"
class ProfileSerializer(serializers.ModelSerializer):
    betting_record = BettingRecordsSerializer(many=True, read_only=True)
    class Meta:
        model = Profile
        fields = "__all__"

class MembersSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False, read_only=True)
    class Meta:
        model = Members
        fields = "__all__"
class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Members
        fields = ('id','email', 'username', 'password1', 'password2')

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields do nt match."})
        password = attrs.get('password1', '')
        if len(password) < 8:
            raise serializers.ValidationError("password must be at least 8 character long")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password1")
        validated_data.pop("password2")
        return Members.objects.create_user(password=password, **validated_data)

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("incorrect credentials")

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"
class PurchasedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchased
        fields = "__all__"
class BuyersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
class DownloadHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DownloadHistory
        fields = "__all__"
class DepositHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositHistory
        fields = "__all__"
class OnwatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Onwatch
        fields = "__all__"
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"