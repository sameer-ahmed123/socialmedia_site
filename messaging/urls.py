from django.urls import path
from messaging.views import Message_template,Directs,SendDirect,search,new_conversation

urlpatterns = [
    path("DM_page/",Message_template, name="Message_template"),
    path("directs/<username>/", Directs, name="directs"),
    path("send/", SendDirect, name="send_direct"),
    path("new/",search, name="user_search"),
    path("new/<username>/", new_conversation, name="new_convo"),
]