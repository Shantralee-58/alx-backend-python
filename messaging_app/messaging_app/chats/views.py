from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ConversationSerializer, UserSerializer, MessageSerializer
from .models import Conversation, User, Message

# Handles conversations between users
class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer

    def get_queryset(self):
        # Return conversations where the user is a participant
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        # Automatically add the current user as a participant if not provided
        if self.request.user not in conversation.participants.all():
            conversation.participants.add(self.request.user)

# Handles messages in conversations
class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        # Return messages only in conversations the user participates in
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the sender as the logged-in user
        serializer.save(sender=self.request.user)

# Handles registration of new users
class UserCreateViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        # Disable GET listing of users from this endpoint
        return User.objects.none()
