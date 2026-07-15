from django.db import transaction
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from providers.models import ProviderProfile
from wallets.models import Transaction as WalletTransaction
from .models import ChatSession, Message
from .serializers import ChatSessionSerializer, MessageSerializer
from .permissions import IsSessionParticipant


class StartChatView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, provider_id):
        try:
            provider = ProviderProfile.objects.get(
                id=provider_id, is_verified=True, is_active=True
            )
        except ProviderProfile.DoesNotExist:
            raise NotFound("Provider not found or not available.")

        if provider.user_id == request.user.id:
            raise ValidationError("You cannot start a chat with yourself.")

        with transaction.atomic():
            wallet = request.user.wallet
            amount = provider.chat_rate

            if wallet.balance < amount:
                raise ValidationError("Insufficient wallet balance. Please deposit first.")

            wallet.balance -= amount
            wallet.held_balance += amount
            wallet.save()

            WalletTransaction.objects.create(
                wallet=wallet,
                type=WalletTransaction.TYPE_CHAT_HOLD,
                amount=amount,
                note=f"Chat started with {provider.display_name}",
            )

            session = ChatSession.objects.create(
                client=request.user,
                provider=provider,
                amount=amount,
            )

        return Response(ChatSessionSerializer(session).data, status=status.HTTP_201_CREATED)


class MyChatSessionsView(generics.ListAPIView):
    serializer_class = ChatSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChatSession.objects.filter(
            models_q_client_or_provider(user)
        ).order_by("-created_at")


def models_q_client_or_provider(user):
    from django.db.models import Q
    return Q(client=user) | Q(provider__user=user)


class ChatSessionDetailView(generics.RetrieveAPIView):
    serializer_class = ChatSessionSerializer
    permission_classes = [permissions.IsAuthenticated, IsSessionParticipant]
    queryset = ChatSession.objects.all()


class CompleteChatView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, session_id):
        try:
            session = ChatSession.objects.get(id=session_id)
        except ChatSession.DoesNotExist:
            raise NotFound("Chat session not found.")

        if session.client_id != request.user.id:
            raise PermissionDenied("Only the client can mark a chat as completed.")

        if session.status != ChatSession.STATUS_ACTIVE:
            raise ValidationError("This chat session is not active.")

        with transaction.atomic():
            client_wallet = session.client.wallet
            provider_wallet = session.provider.user.wallet

            client_wallet.held_balance -= session.amount
            client_wallet.save()

            provider_wallet.balance += session.amount
            provider_wallet.save()

            WalletTransaction.objects.create(
                wallet=provider_wallet,
                type=WalletTransaction.TYPE_CHAT_RELEASE,
                amount=session.amount,
                note=f"Chat completed with {session.client.email}",
            )

            session.status = ChatSession.STATUS_COMPLETED
            session.completed_at = timezone.now()
            session.save()

        return Response(ChatSessionSerializer(session).data)


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_session(self):
        session_id = self.kwargs["session_id"]
        try:
            session = ChatSession.objects.get(id=session_id)
        except ChatSession.DoesNotExist:
            raise NotFound("Chat session not found.")

        user = self.request.user
        if session.client_id != user.id and session.provider.user_id != user.id:
            raise PermissionDenied("You are not part of this chat session.")

        return session

    def get_queryset(self):
        session = self.get_session()
        return Message.objects.filter(session=session).order_by("created_at")

    def perform_create(self, serializer):
        session = self.get_session()

        if session.status != ChatSession.STATUS_ACTIVE:
            raise ValidationError("This chat session is no longer active.")

        serializer.save(session=session, sender=self.request.user)