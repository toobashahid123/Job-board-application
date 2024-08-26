from django.urls import path
from notifications import consumer

websocket_urlpatterns = [
    path('ws/notifications/', consumer.NotificationConsumer.as_asgi()),
]