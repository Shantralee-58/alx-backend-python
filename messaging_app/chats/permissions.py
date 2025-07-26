from rest_framework.permissions import BasePermission

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
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            # obj is Message, check if user is participant of the message's conversation
            return request.user in obj.conversation.participants.all()
        return False

