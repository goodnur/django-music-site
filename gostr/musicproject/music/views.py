from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import MusicFile
from .forms import SimpleRegisterForm

def register_view(request):
    if request.method == 'POST':
        form = SimpleRegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            return redirect('home')
    else:
        form = SimpleRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
        else:
            return render(request, 'login.html', {'form': form, 'error': 'Неверный логин или пароль'})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    if request.method == 'POST' and request.FILES.get('music'):
        file = request.FILES['music']
        MusicFile.objects.create(user=request.user, title=file.name, file=file)
        return redirect('home')

    music_files = MusicFile.objects.filter(user=request.user)
    return render(request, 'home.html', {'music_files': music_files})


