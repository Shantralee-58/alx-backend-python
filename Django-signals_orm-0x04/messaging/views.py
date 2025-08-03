from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import Message

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    
    return redirect('Login')


def home(request):
    return HttpResponse("Welcome to the Messaging app!")


def message_thread_view(request, message_id):
    message = get_object_or_404(Message.objects.select_related('sender', 'receiver'), id=message_id)
    thread = get_message_thread(message)
    return render(request, 'messaging/thread.html', {'thread': thread})

