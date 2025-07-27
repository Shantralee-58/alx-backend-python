from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.http import HttpResponse

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import MessageFilter
from .pagination import MessagePagination


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
        users = User.objects.filter(id__in=participants)
        conversation.participants.set(users)
        conversation.save()
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-sent_at')
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = MessageFilter
    pagination_class = MessagePagination
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']

    def get_queryset(self):
        # Only messages from conversations the user is a participant in
        return Message.objects.filter(conversation__participants=self.request.user)
    

def create(self, request, *args, **kwargs):
    # Support both nested route and JSON body
    conversation_pk = (
        kwargs.get('conversation_pk')
        or request.data.get('conversation_id')
        or request.data.get('conversation')
    )
    sender = request.user
    body = request.data.get('message_body') or request.data.get('content')

    if not (conversation_pk and body):
        return Response({"error": "Missing fields"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        conversation = Conversation.objects.get(pk=conversation_pk)
    except Conversation.DoesNotExist:
        return Response({"error": "Invalid conversation"}, status=status.HTTP_404_NOT_FOUND)

    # Ensure the current user is a participant
    if sender not in conversation.participants.all():
        return Response(
            {"error": "You are not allowed to post in this conversation"},
            status=status.HTTP_403_FORBIDDEN
        )

    # Create message
    message = Message.objects.create(
        conversation=conversation,
        sender=sender,
        message_body=body
    )

    serializer = self.get_serializer(message)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

