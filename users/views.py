from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect


# Create your views here.
class RedirectAuthenticatedUserMixin(UserPassesTestMixin):
    redirect_authenticated_user = True

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            return redirect('home')  # Replace 'home' with the URL you want to redirect authenticated users to
        return super().handle_no_permission()


class RegistrationView(RedirectAuthenticatedUserMixin, View):
    form_class = RegistrationForm
    template_name = "user/registration.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(self.request, f"{form.cleaned_data['username']} registered successfully.")
            return redirect("login")

        return render(request, self.template_name, {"form": form})


class LoginView(RedirectAuthenticatedUserMixin, View):
    form_class = LoginForm
    template_name = "user/login.html"
    redirect_authenticated_user = True

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"{username} logged in successfully.")
                return redirect("home")

        return render(request, self.template_name, {"form": form, 'message': 'Invalid input. Try again.'})

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if request.user.is_authenticated:
            # Set session expiry to 15 days (session cookie)
            request.session.set_expiry(60 * 60 * 24 * 15)
        return response
    

class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        username = request.user.username
        logout(request)
        messages.success(request, f"{username} logged out successfully.")
        return redirect("home")

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login') + '?next=' + self.request.path + '&msg=login_required.')
        return super().handle_no_permission()
        