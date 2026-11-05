from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm
from django.shortcuts import redirect, render
from .models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib import messages

class UserRegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        user  = form.save(commit=False)

        user.is_active = False

        user.save()

        user_token = default_token_generator.make_token(user)
        activation_link = self.request.build_absolute_uri(
            reverse_lazy('user:activate', kwargs={'user_pk': user.pk, 'token': user_token})
        )
        send_mail(
            'Activate your account',
            f'hi {user.username}, \n Please click on link to activate your account: <{activation_link}>',
            '',
            [user.email],
        )
        messages.success(self.request, 'Please check your email to activate your account.')

        return redirect('user:login')

def activate_user(request, user_pk, token):
    user = CustomUser.objects.get(pk=user_pk)

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'You have successfully activated! You can now login.')
        return redirect('user:login')
    messages.warning(request, 'Activation link is invalid or expired.')
    return redirect('/')

class UserLoginView(LoginView):
    template_name = 'user/login.html'
    redirect_authenticated_user = True


def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        try:
            user = CustomUser.objects.filter(email=email, username=username).first()
            token = default_token_generator.make_token(user)
            reset_link = request.build_absolute_uri(
                reverse_lazy('user:password_reset_confirm', kwargs={'user_pk': user.pk, 'token': token})
            )
            send_mail(
                'Reset your password',
                f'Hi {user.username}, \n Please click on link to reset your password: {reset_link}',
                '',
                [user.email],
            )
            messages.success(request, 'Password reset link has been sent to your email.')
            return redirect('user:login')
        except CustomUser.DoesNotExist:
            messages.warning(request, 'User with this email does not exist.')
    return render(request, 'user/password_reset_form.html')


def password_reset_confirm(request, user_pk, token):
    try:
        user = CustomUser.objects.get(pk=user_pk)
    except CustomUser.DoesNotExist:
        messages.warning(request, 'Invalid reset link. Please check your email to reset your password.')
        return redirect('user:login')

    if default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('password')
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password has been successfully reset.')
            return redirect('user:login')
        return render(request, 'user/password_reset_confirm.html')
    else:
        messages.warning(request, 'Password reset link is invalid or expired.')
        return redirect('user:login')
