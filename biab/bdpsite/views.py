import hashlib
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext 
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.models import User

from bdpsite.forms import CaptchaUserCreationForm
from bdpsite.models import *

# Create your views here.

def welcome(request):
    return render_to_response("bdpsite/welcome.html",
        {},
        context_instance=RequestContext(request))

def createuser(request):
    if request.method == 'POST':
        form = CaptchaUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect("/user/login/")
    else:
        form = CaptchaUserCreationForm()

    c={"form":form}
    c.update(csrf(request))
    return render_to_response("bdpsite/newuser.html", c,
        context_instance=RequestContext(request))

def login(request):
    if request.user.is_authenticated():
         return HttpResponseRedirect("/user/%s/"%request.user.username)
    if request.method == 'POST':
        username = request.POST.get("username", '')
        password = request.POST.get("password", '')
        user = auth.authenticate(username = username, 
                                 password = password)
        if user is not None and user.is_active:
            auth.login(request,user)
            return HttpResponseRedirect("/user/%s/"%user.username)
        else:
            c={"username": username,
               "error": _("no such user:password combination")}
    else:
        c={}
    c.update(csrf(request))
    return render_to_response("bdpsite/login.html",c, 
                               context_instance=RequestContext(request))



def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

def profile(request,user):
    user = get_object_or_404(User,username=user) 

    if user.email:
        user.gurl = "https://www.gravatar.com/avatar/%s"%hashlib.md5(user.email).hexdigest()
    else:
        user.gurl = "https://www.gravatar.com/avatar/goo"
     
    c={"profileuser":user}
    return render_to_response("bdpsite/profile.html", c,
        context_instance=RequestContext(request))

