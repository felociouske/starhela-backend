from django.urls import path

from .views import (
    StartChatView,
    MyChatSessionsView,
    ChatSessionDetailView,
    CompleteChatView,
    MessageListCreateView,
)

urlpatterns = [
    path("providers/<int:provider_id>/start-chat/", StartChatView.as_view(), name="start-chat"),
    path("chats/", MyChatSessionsView.as_view(), name="my-chats"),
    path("chats/<int:pk>/", ChatSessionDetailView.as_view(), name="chat-detail"),
    path("chats/<int:session_id>/complete/", CompleteChatView.as_view(), name="chat-complete"),
    path("chats/<int:session_id>/messages/", MessageListCreateView.as_view(), name="chat-messages"),
]