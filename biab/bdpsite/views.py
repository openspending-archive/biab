from django.shortcuts import render_to_response

# Create your views here.

def welcome(request):
    return render_to_response("bdpsite/welcome.html")

def createuser(request):
    pass

def login(request):
    pass

def logout(request):
    pass

