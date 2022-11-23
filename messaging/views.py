from django.shortcuts import render

# Create your views here.

def Message_template(request):

    return render(request, "DMS/Message.html")