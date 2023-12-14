from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import login


def sign_up(request):
    if request.method == 'GET':
        form = UserRegistrationForm()
        context = {
            'form': form,
        }
        return render(request, 'registration/register.html', context)

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have signed up successfully.')
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'registration/register.html', {'form': form})
