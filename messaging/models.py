from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max

# Create your models here.

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name="user")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    recipent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    Message_body = models.CharField(max_length=1200, blank=True, null=True, )
    date = models.DateTimeField(auto_now_add=True)
    is_read =models.BooleanField(default=False)

    def send_message(from_user,to_user, body):   # to create message for both sender and reciver
        sender_message = Message(
           user = from_user,
           sender = from_user,
           recipent = to_user,
           body = body,
           is_read = True
        )
        sender_message.save()

        recipent_message = Message(
            user = to_user,
            sender =from_user,
            recipent = from_user,  #to_user
            body = body,            
        )

        recipent_message.save()
        
        return sender_message 

    def get_messages(user):    # to get recent messages and check count of unreads
        users = []
        messages = Message.objects.filter(user=user).values("recipent").annotate(last=Max('date')).order_by('-last')
        for message in messages:
            users.append({
                'user' : User.objects.get(pk=message['recipent']), 
                'last': message['last'],
                'unread': Message.objects.filter(user=user, recipent__pk=message['recipent'], is_read=False).count()

            })

        return users

    # def __str__(self):
    #     return self.recipent