from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignUpForm, GroupSelectionForm



def group_selection_view(request):
    if request.method == 'POST':
        form = GroupSelectionForm(request.POST)
        if form.is_valid():
            group_name = form.cleaned_data['group'].name
            return redirect('signup', group_name=group_name)
    else:
        form = GroupSelectionForm()
    return render(request, 'account/group_selection.html', {'form': form})


def signup_view(request, group_name):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            
            group = Group.objects.get(name=group_name)
            user.groups.add(group)

            if group_name == 'Customer':
                return redirect('/customer/create/')
            else:
                return redirect('read-redirect')
    else:
        form = SignUpForm()
    
    return render(request, 'account/signup.html', {'form': form, 'group_name': group_name})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("read-redirect")
            else:
                return render(request, 'account/login.html', {'error': 'Invalid Login Credentials'})
    else:
        form = LoginForm()
    return render(request, "account/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("home")

