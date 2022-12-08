from django.shortcuts import render
from messaging.models import Message
from messaging.forms import MessageForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def Message_template(request):
    user = request.user
    messages = Message.get_messages(user=user)
    active_user = None
    directs = None

    if messages:
        message = messages[0]
        active_user = message['user'].username
        directs = Message.objects.filter(user=user, recipent=message['user'])
        directs.update(is_read=True)

        for message in messages:
            if message['user'].username == active_user:
                message['unread'] = 0

    form = MessageForm()
    context = {
        "form": form,
        "directs": directs,
        "messages": messages,
        "active_user": active_user
    }
    return render(request, "DMS/Message.html", context)