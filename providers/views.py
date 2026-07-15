from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from accounts.models import User
from .models import ProviderProfile
from .serializers import ProviderPublicSerializer, ProviderOwnProfileSerializer


class ProviderListView(generics.ListAPIView):
    """Public listing of verified, active providers for clients to browse."""

    serializer_class = ProviderPublicSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = ProviderProfile.objects.filter(is_verified=True, is_active=True)


class ProviderDetailView(generics.RetrieveAPIView):
    serializer_class = ProviderPublicSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = ProviderProfile.objects.filter(is_verified=True, is_active=True)


class MyProviderProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProviderOwnProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        if self.request.user.role != User.ROLE_PROVIDER:
            raise PermissionDenied("Only provider accounts have a provider profile.")

        profile, _ = ProviderProfile.objects.get_or_create(
            user=self.request.user,
            defaults={
                "display_name": self.request.user.username,
                "chat_rate": 50,
            },
        )
        return profile