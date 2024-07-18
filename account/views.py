from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignUpForm


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            
            group_name = form.cleaned_data.get('group')
            if group_name:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)

            return redirect('view-or-write')
            
    else:
        form = SignUpForm()
    
    groups = Group.objects.all()
    return render(request, 'account/signup.html', {'form': form, 'groups': groups})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("view-or-write")
            else:
                return render(request, 'account/login.html', {'error': 'Invalid Login Credentials'})
    else:
        form = LoginForm()
    return render(request, "account/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("home")

