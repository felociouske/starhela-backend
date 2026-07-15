from rest_framework import serializers

from .models import ChatSession, Message


class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source="sender.email", read_only=True)

    class Meta:
        model = Message
        fields = ["id", "session", "sender", "sender_email", "text", "is_auto_reply", "created_at"]
        read_only_fields = ["id", "sender", "sender_email", "is_auto_reply", "created_at"]


class ChatSessionSerializer(serializers.ModelSerializer):
    client_email = serializers.EmailField(source="client.email", read_only=True)
    provider_name = serializers.CharField(source="provider.display_name", read_only=True)

    class Meta:
        model = ChatSession
        fields = [
            "id",
            "client",
            "client_email",
            "provider",
            "provider_name",
            "amount",
            "status",
            "created_at",
            "completed_at",
        ]
        read_only_fields = fields