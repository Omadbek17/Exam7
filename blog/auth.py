from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages
from blog.tokens import account_activation_token

from blog.forms import LoginForm, RegisterForm, EmailForm
from blog.models import User
from django.core.mail import send_mail
from config.settings import DEFAULT_FROM_EMAIL
from django.views.generic import View
from blog.forms import LoginForm, RegisterForm



class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'blog/auth/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
            else:
                messages.add_message(
                    request,
                    level=messages.WARNING,
                    message='User not found'
                )

        return render(request, 'blog/auth/login.html', {'form': form})



class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect(reverse('index'))

    def post(self, request):
        return render(request, 'blog/auth/logout.html')



class RegisterView(View):

    def get(self, request):
        form = RegisterForm()
        return render(request, 'blog/auth/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = User.objects.create_user(first_name=first_name, email=email, password=password)
            user.is_active = False
            user.is_staff = True
            user.is_superuser = True
            user.save()

            current_site = get_current_site(request)
            subject = 'Verify your email'
            message = render_to_string('blog/auth/activation.html', {
                'request': request,
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': account_activation_token.make_token(user),
            })

            email = EmailMessage(subject, message, to=[email])
            email.content_subtype = 'html'
            email.send()

            return redirect('verify_email_done')

        return render(request, 'blog/auth/register.html', {'form': form})


