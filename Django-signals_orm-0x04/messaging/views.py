from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    
    return redirect('Login')


def home(request):
    return HttpResponse("Welcome to the Messaging app!")

