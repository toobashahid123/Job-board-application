from django.urls import path, include
# from .views import NotificationViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]