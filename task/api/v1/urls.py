# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from task.views import UserViewSet

router = DefaultRouter()
# router.register(r'profiles', UserProfileViewSet, basename='userprofile')
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path('', include(router.urls)),
]
