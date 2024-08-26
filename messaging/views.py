from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Message
from .serializers import MessageSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


def chat_room(request, room_name):
    return render(request, 'chat.html', {
        'room_name': room_name
    })    