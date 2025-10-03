from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.ChatRoomListCreateView.as_view(), name='chatroom-list-create'),
    path('rooms/<int:pk>/', views.ChatRoomDetailView.as_view(), name='chatroom-detail'),
    path('rooms/<int:chat_room_id>/messages/', views.MessageListCreateView.as_view(), name='message-list-create'),
    path('rooms/<int:chat_room_id>/mark-read/', views.MarkMessagesReadView.as_view(), name='mark-messages-read'),
]