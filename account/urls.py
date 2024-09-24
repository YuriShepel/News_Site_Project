from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomAuthenticationForm

app_name = 'account'
urlpatterns = [
    # path('login/', views.user_login, name='login'),
       path('login/', auth_views.LoginView.as_view(authentication_form=CustomAuthenticationForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
