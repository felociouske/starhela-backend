from rest_framework.permissions import BasePermission


class IsSessionParticipant(BasePermission):
    def has_object_permission(self, request, view, obj):
        session = obj if hasattr(obj, "client") else obj.session
        user = request.user
        return session.client_id == user.id or session.provider.user_id == user.id