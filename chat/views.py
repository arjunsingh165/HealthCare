from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db import models
from .models import ChatRoom, Message
from .serializers import (
    ChatRoomSerializer, ChatRoomCreateSerializer,
    MessageSerializer, MessageCreateSerializer
)
from accounts.permissions import IsAppointmentParticipant, IsAdminUser

class ChatRoomListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering = ['-updated_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return ChatRoom.objects.all()
        else:
            return ChatRoom.objects.filter(
                models.Q(patient=user) | models.Q(doctor=user)
            )
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ChatRoomCreateSerializer
        return ChatRoomSerializer


class ChatRoomDetailView(generics.RetrieveAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAppointmentParticipant]


class MessageListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering = ['timestamp']
    
    def get_queryset(self):
        chat_room_id = self.kwargs.get('chat_room_id')
        chat_room = ChatRoom.objects.get(id=chat_room_id)
        
        # Check if user is participant in this chat room
        user = self.request.user
        if user not in [chat_room.patient, chat_room.doctor] and user.role != 'admin':
            return Message.objects.none()
        
        return Message.objects.filter(chat_room_id=chat_room_id)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MessageCreateSerializer
        return MessageSerializer
    
    def create(self, request, *args, **kwargs):
        chat_room_id = self.kwargs.get('chat_room_id')
        try:
            chat_room = ChatRoom.objects.get(id=chat_room_id)
        except ChatRoom.DoesNotExist:
            return Response(
                {'error': 'Chat room not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if user is participant in this chat room
        user = request.user
        if user not in [chat_room.patient, chat_room.doctor]:
            return Response(
                {'error': 'You are not a participant in this chat room'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Add chat_room to request data
        request.data['chat_room'] = chat_room_id
        return super().create(request, *args, **kwargs)


class MarkMessagesReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, chat_room_id):
        try:
            chat_room = ChatRoom.objects.get(id=chat_room_id)
        except ChatRoom.DoesNotExist:
            return Response(
                {'error': 'Chat room not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if user is participant in this chat room
        user = request.user
        if user not in [chat_room.patient, chat_room.doctor]:
            return Response(
                {'error': 'You are not a participant in this chat room'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Mark all messages as read except sender's own messages
        Message.objects.filter(
            chat_room=chat_room,
            is_read=False
        ).exclude(sender=user).update(is_read=True)
        
        return Response({'message': 'Messages marked as read'})


class ChatStatsView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        total_chat_rooms = ChatRoom.objects.count()
        active_chat_rooms = ChatRoom.objects.filter(is_active=True).count()
        total_messages = Message.objects.count()
        
        stats = {
            'total_chat_rooms': total_chat_rooms,
            'active_chat_rooms': active_chat_rooms,
            'total_messages': total_messages,
        }
        return Response(stats)