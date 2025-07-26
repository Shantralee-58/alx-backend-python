from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.http import HttpResponse

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation


def home(request):
    return HttpResponse("Welcome to the Messaging App API!")


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Users only see conversations they participate in
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request):
        participants = request.data.get('participants')
        if not participants:
            return Response({"error": "Participants required"}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        users = User.objects.filter(user_id__in=participants)
        conversation.participants.set(users)
        conversation.save()
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Only messages from conversations the user is a participant in
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request):
        conversation_id = request.data.get('conversation')
        sender_id = request.data.get('sender')
        body = request.data.get('message_body')

        if not (conversation_id and sender_id and body):
            return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation = Conversation.objects.get(pk=conversation_id)
            sender = User.objects.get(pk=sender_id)
        except (Conversation.DoesNotExist, User.DoesNotExist):
            return Response({"error": "Invalid conversation or sender"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the current user is a participant in this conversation
        if request.user not in conversation.participants.all():
            return Response({"error": "You are not allowed to post in this conversation"},
                            status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(conversation=conversation, sender=sender, message_body=body)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

