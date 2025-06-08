import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from task.serializers import UserProfileSerializer, UserSerializer
from task.models import UserProfile
from django.db import transaction
from task.models import UserProfile
from task.serializers import UserSerializer
User = get_user_model()

@pytest.fixture
def user_data():
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'profile': {
            'website': 'https://example.com',
            'bio': 'This is a test bio that is more than 50 characters long to satisfy the validation requirement.'
        }
    }

@pytest.fixture
def user_profile_data():
    return {
        'website': 'https://example.com',
        'bio': 'This is a test bio that is more than 50 characters long to satisfy the validation requirement.'
    }

@pytest.mark.django_db
class TestUserProfileSerializer:
    def test_valid_profile_data(self, user_profile_data):
        serializer = UserProfileSerializer(data=user_profile_data)
        assert serializer.is_valid()
        assert serializer.validated_data == user_profile_data

    def test_invalid_bio_length(self):
        invalid_data = {
            'website': 'https://example.com',
            'bio': 'Too short bio'
        }
        serializer = UserProfileSerializer(data=invalid_data)
        assert not serializer.is_valid()
        assert 'bio' in serializer.errors

    def test_empty_bio(self):
        data = {
            'website': 'https://example.com',
            'bio': ''
        }
        serializer = UserProfileSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data['bio'] == ''

@pytest.mark.django_db
class TestUserSerializer:
    def test_create_user_with_profile(self, user_data):
     
        # Create the user first
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )
        
        # Now create the profile using the serializer
        profile_serializer = UserProfileSerializer(data=user_data['profile'])
        assert profile_serializer.is_valid()
        profile = profile_serializer.save(user=user)
        
        # Verify the data
        assert user.username == user_data['username']
        assert user.email == user_data['email']
        assert user.first_name == user_data['first_name']
        assert user.last_name == user_data['last_name']
        assert profile.website == user_data['profile']['website']
        assert profile.bio == user_data['profile']['bio']

    def test_update_user_and_profile(self, user_data):
        # First create a user and profile
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password='testpass123',
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )
        profile = UserProfile.objects.create(
            user=user,
            website=user_data['profile']['website'],
            bio=user_data['profile']['bio']
        )

        # Update data
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'profile': {
                'website': 'https://updated.com',
                'bio': 'This is an updated bio that is more than 50 characters long to satisfy the validation requirement.'
            }
        }
        
        serializer = UserSerializer(user, data=update_data, partial=True)
        assert serializer.is_valid()
        updated_user = serializer.save()

        # Refresh from database
        updated_user.refresh_from_db()
        updated_user.profile.refresh_from_db()

        assert updated_user.first_name == 'Updated'
        assert updated_user.last_name == 'Name'
        assert updated_user.profile.website == 'https://updated.com'
        assert updated_user.profile.bio == 'This is an updated bio that is more than 50 characters long to satisfy the validation requirement.'




User = get_user_model()

@pytest.mark.django_db
def test_create_user_with_profile():
    data = {
        "username": "ahmed",
        "email": "ahmed@example.com",
        "first_name": "Ahmed",
        "last_name": "Goda",
        "profile": {
            "website": "https://ahmed.dev",
            "bio": "I am a Django developer with more than 1 year of experience."
        }
    }
    serializer = UserSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    user = serializer.save()
    assert User.objects.count() == 1
    assert user.profile.website == "https://ahmed.dev"


@pytest.mark.django_db
def test_update_user_profile():
    user = User.objects.create(username="ahmed", email="old@example.com")
    UserProfile.objects.create(user=user, website="https://old.dev", bio="Old bio text with enough characters.")

    update_data = {
        "email": "new@example.com",
        "profile": {
            "website": "https://new.dev",
            "bio": "Updated bio with at least 50 characters for test coverage."
        }
    }
    serializer = UserSerializer(instance=user, data=update_data, partial=True)
    assert serializer.is_valid(), serializer.errors
    updated_user = serializer.save()
    assert updated_user.email == "new@example.com"
    assert updated_user.profile.website == "https://new.dev"


@pytest.mark.django_db
def test_invalid_bio_length():
    data = {
        "username": "shortbio",
        "email": "short@example.com",
        "profile": {
            "website": "https://short.com",
            "bio": "Too short"
        }
    }
    serializer = UserSerializer(data=data)
    assert not serializer.is_valid()
    assert "bio" in serializer.errors['profile']


