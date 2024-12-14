from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Buyers, Message, Members, DepositHistory


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = Members
        fields = ("email",)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Members
        fields = ("email",)

class Buyer(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Password", required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password", required=True)
    class Meta:
        model = Buyers
        fields = ("username", "email",)

class Messages(ModelForm):

    class Meta:
        model = Message
        fields = ('email', 'message')
class DepositForm(ModelForm):
     class Meta:
        model = DepositHistory
        fields = ('amount',)