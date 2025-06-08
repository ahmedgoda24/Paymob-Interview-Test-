from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile
from django.db import transaction
from .utils import CoreUtils
User = get_user_model()
class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = ['website', 'bio']
    
    def validate_bio(self, value):
        if value and len(value) < 50:
            raise serializers.ValidationError("Bio must be at least 50 characters long")
        return value

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        with transaction.atomic():
            if profile_data:
                CoreUtils.serializer_save(
                    UserProfileSerializer,
                    instance=instance.profile,
                    data=profile_data,
                    partial=True
                )
                # profile_serializer = UserProfileSerializer(instance.profile, data=profile_data, partial=True)
                # profile_serializer.is_valid(raise_exception=True)
                # profile_serializer.save()
        # Update user fields
        return super().update(instance, validated_data)





######################################################################################

    
