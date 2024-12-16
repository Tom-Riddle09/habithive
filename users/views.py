from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('habits:dashboard') # dashboard page inside habit app. -redirect url = [habits:dashboard]
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form':form})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password = password)
        if user is not None:
            login(request, user)
            return redirect('habits:dashboard') # [habits:dashboard]
        else:
            return render(request, 'users/login.html', {'error':'Invalid username or password'})
    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('users:login')

@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('users:login') #redirect to login page after account deletion
    return render(request, 'users/delete_account.html')