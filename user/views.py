from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm


class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('user:login')


class UserLoginView(LoginView):
    template_name = 'user/login.html'
    redirect_authenticated_user = True


