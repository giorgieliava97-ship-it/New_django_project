from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView
from .views import UserRegisterView, UserLoginView, activate_user,password_reset_request, password_reset_confirm

app_name = 'user'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('user:login')), name='logout'),
    path('activate/<int:user_pk>/<token>/', activate_user, name='activate'),
    path('password-reset/', password_reset_request, name='password_reset'),
    path('password-reset-confirm/<int:user_pk>/<token>/', password_reset_confirm, name='password_reset_confirm'),
]