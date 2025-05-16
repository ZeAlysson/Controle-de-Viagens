from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_servidores, name='login'),
    path('login/admin', auth_views.LoginView.as_view(template_name='login/admin/login.html'), name='login_admin'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registrar_usuario, name='registro'),
    path('logado/', views.logado, name='logado'),
    
]