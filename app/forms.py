from dataclasses import fields
from pyexpat import model
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import Posts, Comments

class login_form(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-lg ", "id": "id_username","autofocus": True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "current-password","class": "form-control form-control-lg","autofocus": True}))



class postCreateForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = (
            'post_name',
            'desription',
            'image'
        )
        widgets = {
             'post_name': forms.TextInput(attrs={"class": "form-control "}),
            'desription': forms.Textarea(attrs={"class": "form-control ", "rows":4}),
            'image': forms.FileInput(attrs={"class": "form-control"})
        }
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('comment','post','user')
