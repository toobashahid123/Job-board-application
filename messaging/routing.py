from django.urls import path
from . import consumer

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', consumer.ChatConsumer.as_asgi()),
    # re_path(r'ws/chat/(?P<room_name>\w+)/$', consumer.ChatConsumer.as_asgi()),
]