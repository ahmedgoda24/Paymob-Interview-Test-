# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from task1.views import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('api/v1/task1/', include(router.urls)),
   
]
