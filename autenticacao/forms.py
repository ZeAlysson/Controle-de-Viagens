from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginForm(UserCreationForm):
    
    class meta:
        model = User
        fields = ["username", "password"]

class LoginServidoresForm(forms.Form):
    cpf = forms.CharField(
        max_length=11,
        label="CPF",
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu CPF', 'class': 'form-control'})
    )