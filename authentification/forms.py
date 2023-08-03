from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


# Class form authentication
class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label="Nom d'utilisateur",
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=63, label="mot de passe",
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control'}))


# Class form inscription   
class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')
        # Add widgets for the style
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),

}