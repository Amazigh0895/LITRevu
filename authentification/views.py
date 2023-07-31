from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from . import forms


# Create your views here.

# Login page  function
def login_page(request):
    form = forms.LoginForm()
    message = ""
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                # Connecte our user if the authentication succeed
                login(request, user)
                message = f'Bonjour, {user.username}! vous etes connecté'
            else:
                # Get error message if our autheticaton doesnt succeed
                message = " identifiants invalides"
    else:
        form = forms.LoginForm()
    # Send form and message to login.html  page
    return render(request, 'authentification/login.html',
                  context={'from': form, 'message': message})


# Logout user function
def logout_user(request):

    # There we logout our user
    logout(request)
    return redirect('login-page')
