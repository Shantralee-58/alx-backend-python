from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import Message
from django.views.decorators.cache import cache_page


@login_required
@cache_page(60)  # Caches for 60 seconds
def conversation_messages(request):
    # Fetch all messages involving the current user
    messages = (
        Message.objects.filter(receiver=request.user)
        .select_related('sender')
        .order_by('-timestamp')
    )
    return render(request, 'messaging/conversation_messages.html', {'messages': messages})


def unread_messages(request):
    # Use the custom manager method explicitly
    messages = Message.unread.unread_for_user(request.user).only(
        'id', 'content', 'timestamp', 'sender'
    )

    return render(request, 'messaging/unread_messages.html', {'messages': messages})
 


def delete_user(request):
    user = request.user
    user.delete()
    
    return redirect('Login')


def home(request):
    return HttpResponse("Welcome to the Messaging app!")


def get_message_thread(message):
    """
    Recursively get message and all its replies in threaded format.
    """
    # Prefetch replies and optimize sender and receiver fetching
    replies = Message.objects.filter(parent_message=message).select_related('sender', 'receiver').prefetch_related('replies')
    thread_replies = [get_message_thread(reply) for reply in replies]

    return {
        'message': message,
        'replies': thread_replies,
    }

def message_thread_view(request, message_id):
    # Fetch message with related sender and receiver to reduce DB hits
    message = get_object_or_404(Message.objects.select_related('sender', 'receiver'), id=message_id)
    
    # Get the entire thread recursively
    thread = get_message_thread(message)

    return render(request, 'messaging/thread.html', {'thread': thread})

def user_messages(request):
    # Fetch messages sent by the current logged-in user,
    # use select_related for 'receiver' and 'parent_message' to avoid extra queries,
    # prefetch replies if needed.
    messages = (
        Message.objects.filter(sender=request.user)
        .select_related('receiver', 'parent_message')
        .prefetch_related('message_set')  # message_set is the reverse relation for replies
    )

    context = {
        'messages': messages,
    }
    return render(request, 'messaging/user_messages.html', context)

