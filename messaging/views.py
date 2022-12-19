from django.shortcuts import render,redirect
from messaging.models import Message
from django.http import HttpResponseBadRequest
from messaging.forms import DirectForm
from django.contrib.auth.models import User
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

    form = DirectForm()
    context = {
        "form": form,
        "directs": directs,
        "messages": messages,
        "active_user": active_user
    }
    return render(request, "DMS/Message.html", context)

@login_required
def Directs(request, username):
    user = request.user
    messages = Message.get_messages(user=user)
    active_direct = username
    directs = Message.objects.filter(user=user, recipent=username)
    directs.update(is_read=True)

    for message in messages:
        if message['user'].username == username:
            message['unread'] = 0
    form = DirectForm()
    context = {
        "form": form,
        "directs":directs,
        "messages": messages,
        "active_direct":active_direct,
    }
    return render(request, "DMS/Message.html", context)


@login_required
def SendDirect(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    print(to_user_username)
    Message_body = request.POST.get('Message_body')
    print(Message_body)

    if request.method =="POST":
        to_user = User.objects.get(id= to_user_username)
        Message.send_message(from_user, to_user, Message_body)
        return redirect('Message_template')
    else:
        HttpResponseBadRequest("bad reuest")