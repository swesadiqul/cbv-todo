from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

#create forms here
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']