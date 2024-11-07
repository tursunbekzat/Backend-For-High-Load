# tasks/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from .tasks import send_email_task
from .forms import EmailForm 



def profile(request):
    return HttpResponse("Welcome to the Profile Page!")

def home(request):
    return HttpResponse("Welcome to the Home Page!") 

def send_email_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.save()
            # Queue the task to send email asynchronously
            send_email_task.delay(email.recipient, email.subject, email.body)
            messages.success(request, 'Email is being sent in the background.')
            return redirect('send_email')
    else:
        form = EmailForm()
    return render(request, 'tasks/send_email.html', {'form': form})