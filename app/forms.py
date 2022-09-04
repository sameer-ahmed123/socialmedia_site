from django.contrib.auth.forms import AuthenticationForm
from django import forms


class login_form(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "id": "form2Example17","autofocus": True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "current-password","class": "form-control form-control-lg"}))