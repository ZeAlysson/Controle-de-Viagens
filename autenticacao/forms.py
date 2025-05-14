from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


# Alterar LoginForm para usar AuthenticationForm
class AdminLoginForm(AuthenticationForm): # Renomear e mudar a herança
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de Usuário', 'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}))
    
    # Remover a classe Meta interna se não for customizar o modelo ou campos do AuthenticationForm
    # class Meta: # Esta Meta não é típica para AuthenticationForm, a menos que você esteja fazendo algo muito customizado
    #     model = User
    #     fields = ["username", "password"]

class LoginServidoresForm(forms.Form):
    cpf = forms.CharField(
        max_length=11,
        label="CPF",
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu CPF', 'class': 'form-control'})
    )