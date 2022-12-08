from django import forms
from messaging.models import Message

class MessageForm(forms.ModelForm):

    class Meta():
        model = Message
        fields = ['body']

        widgets = {
            "body": forms.TextInput(attrs={"id": "message_input", "name": "forms.py_form"})
        }
