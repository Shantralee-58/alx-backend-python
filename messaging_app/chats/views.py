from rest_framework import viewsets
from rest_framework.response import Response

class ConversationViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response({"message": "Conversation list"})

class MessageViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response({"message": "Message list"})

class UserCreateViewSet(viewsets.ViewSet):
    def create(self, request):
        return Response({"message": "User created"})

