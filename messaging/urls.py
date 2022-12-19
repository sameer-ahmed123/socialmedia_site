from django.urls import path
from messaging.views import Message_template,Directs,SendDirect

urlpatterns = [
    path("DM_page/",Message_template, name="Message_template"),
    path("directs/<username>/", Directs, name="directs"),
    path("send/", SendDirect, name="send_direct"),
]