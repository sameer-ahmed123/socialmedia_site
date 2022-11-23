from django.urls import path
from messaging.views import Message_template

urlpatterns = [
    path("DM_page/",Message_template, name="Message_template"),
]