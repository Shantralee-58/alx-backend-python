from .models import User, Conversation, Message
from rest_framework import serializers

# ========================
# User Serializer
# ========================
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'user_id', 'email', 'first_name', 'last_name',
            'phone_number', 'password', 'role', 'full_name'
        ]
        read_only_fields = ['user_id', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

# ========================
# Message Serializer
# ========================
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # Shows full sender details

    class Meta:
        model = Message
        fields = [
            'message_id', 'sender', 'conversation',
            'message_body', 'sent_at'
        ]
        read_only_fields = ['message_id', 'sent_at', 'sender']

# ========================
# Conversation Serializer
# ========================
class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True
    )
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants', 'created_at', 'messages'
        ]
        read_only_fields = ['conversation_id', 'created_at', 'messages']

