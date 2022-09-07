from dataclasses import fields
from pyexpat import model
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import Posts

class login_form(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "id": "form2Example17","autofocus": True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "current-password","class": "form-control form-control-lg"}))



class postCreateForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = (
            'post_name',
            'desription',
            'image'
        )

    
