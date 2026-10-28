from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import UserRegisterView, UserLoginView

app_name = 'user'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='store:index'), name='logout'),
]