from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from . import forms


# Create your views here.

# Login page  function
def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:

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
                    #message = f'Bonjour, {user.username}! vous etes connecté'
                    return redirect('home')
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


# Signup fonction
def sign_up(request):
    message = ""
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = forms.SignUpForm()
        if request.method == 'POST':
            form = forms.SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('home')
            else:
                message = "Erreur de saisie !"
        else:
            form = forms.SignUpForm()
        context = {
            'form': form,
            'message': message,
        }    
        return render(request, 'authentification/signup.html',context=context)