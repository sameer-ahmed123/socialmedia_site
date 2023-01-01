from django import forms
from messaging.models import Message

class DirectForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('Message_body',)
        widgets  = {
            'Message_body': forms.TextInput(attrs={"id": "message_input","autocomplete":"off"})  
        }
