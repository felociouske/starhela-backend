from rest_framework import serializers

from .models import ProviderProfile


class ProviderPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderProfile
        fields = [
            "id",
            "display_name",
            "bio",
            "nationality",
            "photo",
            "chat_rate",
            "is_verified",
        ]
        read_only_fields = fields


class ProviderOwnProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderProfile
        fields = [
            "id",
            "display_name",
            "bio",
            "nationality",
            "photo",
            "chat_rate",
            "is_verified",
            "is_active",
            "id_document",
            "created_at",
        ]
        read_only_fields = ["id", "is_verified", "created_at"]