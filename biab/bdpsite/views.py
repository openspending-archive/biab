import hashlib
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.template.context import RequestContext 
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from genname.generate import generate_name

from bdpsite.forms import CaptchaUserCreationForm, CreateForm, ProjectForm
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
    projects = Project.objects.filter(creator = user)     
    c={"profileuser":user,
        "projects": projects}
    return render_to_response("bdpsite/profile.html", c,
        context_instance=RequestContext(request))

@login_required
def create(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            # Kick off loading process
            # create empty project
            p = Project()
            # fill project with random name and slug
            p.title = generate_name()
            p.slug = slugify(unicode(p.title))
            p.creator = request.user
            p.save()
            return HttpResponseRedirect("/%s/edit/"%p.slug)
    else:
        form = CreateForm()
    c={"form": form}
    c.update(csrf(request))
    return render_to_response("bdpsite/create.html", c,
        context_instance = RequestContext(request))

@login_required
def editproject(request,project):
    project = get_object_or_404(Project, slug = project)
    if project.creator != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance = project)
        if form.is_valid():
            form.save()
    else:
        form = ProjectForm(instance = project)

    c={"form":form,
       "project": project,
       "page": "edit"}
    c.update(csrf(request))
    return render_to_response("bdpsite/editproject.html", c,
        context_instance = RequestContext(request))

@login_required
def packages(request,project):
    project = get_object_or_404(Project, slug = project)
    if project.creator != request.user:
        return HttpResponseForbidden()
    datapackages = DataPackage.objects.filter(project = project)
    c={"project": project,
       "datapackages": datapackages,
       "page": "packages"}
    return render_to_response("bdpsite/packages.html", c,
        context_instance = RequestContext(request))

def project(request,project):
    project = get_object_or_404(Project, slug = project)
    visualizations = Visualization.objects.raw("""
        select id from bdpsite_visualization where dataset_id in
            (select id from bdpsite_dataset where datapackage_id in 
                (select id from bdpsite_datapackage where project_id =
                %s));"""%project.id)
    c = {"project": project,
         "visualizations": visualizations}
    return render_to_response("bdpsite/project.html", c,
        context_instance = RequestContext(request))
