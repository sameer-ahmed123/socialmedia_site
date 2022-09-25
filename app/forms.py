from dataclasses import fields
from pyexpat import model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from .models import Posts, Comments, User

class login_form(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control form-control-lg ", "id": "id_username","autofocus": True,"list":"id_usernames"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "current-password","class": "form-control form-control-lg","autofocus": True}))


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={"class": "form-control "}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={"class": "form-control ", "id":"usernames"}),
            'password1': forms.TextInput(attrs={"class": "form-control"}),
            'password2': forms.TextInput(attrs={"class": "form-control"})

        }
    def __init__(self, *args, **kwargs):
            super(RegisterForm, self).__init__(*args, **kwargs)

            self.fields['password1'].widget.attrs["class"] = "form-control"
            self.fields['password2'].widget.attrs["class"] = "form-control"   


    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user 

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
    
# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comments
#         fields = ('comment','post','user')
