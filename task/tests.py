from django.test import TestCase
from django.contrib.auth import get_user_model 
from rest_framework.exceptions import ValidationError
from task.serializers import UserProfileSerializer, UserSerializer
from task.models import UserProfile
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status


class UserProfileSerializerTest(TestCase):
    def test_validate_bio_valid(self):
        serializer = UserProfileSerializer()
        bio = "This is a valid bio with more than 50 characters. It is descriptive and detailed."
        validated_bio = serializer.validate_bio(bio)
        self.assertEqual(validated_bio, bio)

    def test_validate_bio_invalid(self):
        serializer = UserProfileSerializer()
        bio = "Short bio"
        with self.assertRaises(ValidationError) as context:
            serializer.validate_bio(bio)
        self.assertEqual(str(context.exception.detail[0]), "Bio must be at least 50 characters long")


class UserSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "profile": {
                "website": "https://example.com",
                 "bio": "This is a valid bio with more than 50 characters. It is descriptive and detailed."
            }
        }
        self.User = get_user_model()

    def test_create_user_with_profile(self):
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()

        self.assertEqual(user.username, self.user_data["username"])
        self.assertEqual(user.email, self.user_data["email"])
        self.assertEqual(user.first_name, self.user_data["first_name"])
        self.assertEqual(user.last_name, self.user_data["last_name"])
        self.assertEqual(user.profile.website, self.user_data["profile"]["website"])
        self.assertEqual(user.profile.bio, self.user_data["profile"]["bio"])



    def test_update_user_with_profile(self):
        user = self.User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            first_name="Test",
            last_name="User"
        )
        profile = UserProfile.objects.create(
            user=user,
            website="https://example.com",
            bio="This is an old bio with more than 50 characters. It is descriptive and detailed."
        )

        updated_data = {
            "username": "updateduser",
            "email": "updateduser@example.com",
            "first_name": "Updated",
            "last_name": "User",
            "profile": {
                "website": "https://updated.com",
                "bio": "This is an updated bio with more than 50 characters. It is descriptive and detailed."
            }
        }

        serializer = UserSerializer(instance=user, data=updated_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_user = serializer.save()

        self.assertEqual(updated_user.username, updated_data["username"])
        self.assertEqual(updated_user.email, updated_data["email"])
        self.assertEqual(updated_user.first_name, updated_data["first_name"])
        self.assertEqual(updated_user.last_name, updated_data["last_name"])
        self.assertEqual(updated_user.profile.website, updated_data["profile"]["website"])
        self.assertEqual(updated_user.profile.bio, updated_data["profile"]["bio"])
        User = get_user_model()

