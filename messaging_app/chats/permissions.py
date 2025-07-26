from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation
    to view or edit messages in that conversation.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users globally
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # obj can be Conversation or Message
        if hasattr(obj, 'participants'):
            # obj is Conversation
            is_participant = request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            # obj is Message, check if user is participant of the message's conversation
            is_participant = request.user in obj.conversation.participants.all()
        else:
            return False

        # Explicitly restrict methods: GET, POST, PUT, PATCH, DELETE
        if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            return is_participant
        return False

