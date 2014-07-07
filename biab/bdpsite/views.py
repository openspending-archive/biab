import hashlib
import urllib2
import json
import dateutil.parser
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotFound
from django.template.context import RequestContext 
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from genname.generate import generate_name
from django.forms.util import ErrorList

from bdpsite.forms import *
from bdpsite.models import *
from bdpsite.tasks import *

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
            #p.slug = slugify(unicode(p.title))
            p.creator = request.user
            p.save()
            # create new data package;
            # use Celery to do this asynchronously...
            create_bdp.delay(p, form.cleaned_data["url"])
            return HttpResponseRedirect("/%s/edit/"%p.slug)
    else:
        form = CreateForm()
    c={"form": form}
    c.update(csrf(request))
    return render_to_response("bdpsite/create.html", c,
        context_instance = RequestContext(request))

@login_required
def createbare(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user
            project.save()
            return HttpResponseRedirect("/%s/datasets/"%project.slug)
    else:
        form = ProjectForm()

    c = {"form": form}
    c.update(csrf(request))
    return render_to_response("bdpsite/createbare.html", c,
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
            if form.cleaned_data['slug'] != project:
                return HttpResponseRedirect("/%s/edit/"%form.cleaned_data['slug'])
    else:
        form = ProjectForm(instance = project)

    c={"form":form,
       "project": project,
       "page": "edit"}
    c.update(csrf(request))
    return render_to_response("bdpsite/editproject.html", c,
        context_instance = RequestContext(request))

@login_required
def package(request,project,package):
    project = get_object_or_404(Project, slug = project)
    package = get_object_or_404(DataPackage, slug = package)
    if project.creator != request.user:
        return HttpResponseForbidden()
    datasets = Dataset.objects.filter(datapackage = package)
    if request.method == 'POST':
        form = DataPackageForm(request.POST, instance=package)
        if form.is_valid():
            form.save()
            if form.cleaned_data['slug'] != package:
                return HttpResponseRedirect("/%s/packages/package/%s"%(project.slug, package.slug))
    else:
        form = DataPackageForm(instance = package)
    c = {
        "form": form,
        "project": project,
        "package": package,
        "datasets": datasets,
        "page": "package"
    }
    c.update(csrf(request))
    return render_to_response("bdpsite/package.html", c,
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

@login_required
def addpackage(request,project):
    project = get_object_or_404(Project, slug = project)
    if project.creator != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            # create new data package;
            # use Celery to do this asynchronously...
            create_bdp.delay(project, form.cleaned_data["url"], form.cleaned_data["auto_upload"])
            return HttpResponseRedirect("../")
    else:
        form = CreateForm()
    c={"form": form}
    c.update(csrf(request))
    return render_to_response("bdpsite/addpackage.html", c,
        context_instance = RequestContext(request))

@login_required
def datasets(request,project):
    project = get_object_or_404(Project, slug = project)
    if project.creator != request.user:
        return HttpResponseForbidden()
    datasets = Dataset.objects.filter(project = project)
    c={"project": project,
       "datasets": datasets,
       "page": "datasets" }
    return render_to_response("bdpsite/datasets.html", c,
        context_instance = RequestContext(request))

@login_required
def adddataset(request,project):
    project = get_object_or_404(Project, slug = project)
    if project.creator != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = AddDatasetForm(request.POST)
        if form.is_valid():
            s = form.cleaned_data['slug']
            try:
                u = urllib2.urlopen("https://openspending.org/%s.json"%s)
                data = json.load(u)
                d = Dataset()
                d.name = data['name']
#                d.path = u
# The path needs to be the raw CSV... Which we don't get from OS
                d.openspending = "https://openspending.org/%s/"%s
                d.type = data['category']
                d.currency = data['currency']
                d.dateLastUpdated = dateutil.parser.parse(
                    data['timestamps']['last_modified'])
                d.datePublished = dateutil.parser.parse(
                    data['timestamps']['created'])
                d.description = data['description']
                d.project = project
                d.save()
                return HttpResponseRedirect("../")
            except urllib2.HTTPError:
                errors =form._errors.setdefault("slug", ErrorList())
                errors.append(u"Can not find dataset or openspending unreachable")
    else:
        form = AddDatasetForm()
    c={"project": project,
        "page":"datasets",
        "form": form }
    c.update(csrf(request))    
    return render_to_response("bdpsite/adddataset.html", c,
        context_instance = RequestContext(request))

@login_required
def deletedataset(request,project,id): 
    dataset = get_object_or_404(Dataset, id=id)
    if dataset.project.creator != request.user or dataset.project.slug != project:
        return HttpResponseForbidden()
    dataset.delete()
    return HttpResponseRedirect("../../")

@login_required
def deletepackage(request,project,id): 
    package = get_object_or_404(DataPackage, id=id)
    if package.project.creator != request.user or package.project.slug != project:
        return HttpResponseForbidden()
    package.delete()
    return HttpResponseRedirect("../../")


@login_required
def preprocessdataset(request,project,id):
    dataset = get_object_or_404(Dataset, id=id)
    if dataset.project.creator != request.user or dataset.project.slug != project:
        return HttpResponseForbidden()
    result = preprocess_dataset.delay({}, id).get(propagate=False)
    return HttpResponse(json.dumps(result), mimetype="application/json")

@login_required
def generatemodel(request,project,id):
    dataset = get_object_or_404(Dataset, id=id)
    if dataset.project.creator != request.user or dataset.project.slug != project:
        return HttpResponseForbidden()
    result = generate_model.delay({}, id).get(propagate=False)
    return HttpResponse(json.dumps(result), mimetype="application/json")

@login_required
def osuploaddataset(request,project,id):
    dataset = get_object_or_404(Dataset, id=id)
    if dataset.project.creator != request.user or dataset.project.slug != project:
        return HttpResponseForbidden()
    result = osload.delay({}, id).get(propagate=False)
    return HttpResponse(json.dumps(result), mimetype="application/json")

@login_required
def visualizations(request,project):    
    project = get_object_or_404(Project, slug = project)
    if project.creator != request.user:
        return HttpResponseForbidden()
    visualizations = Visualization.objects.raw("""
        select id from bdpsite_visualization where dataset_id in (
            select id from bdpsite_dataset where project_id=
            %s) order by 'order'"""%project.id)
    c={"project":project,
        "visualizations": visualizations,
        "page":"viz"}
    return render_to_response("bdpsite/visualizations.html", c,
        context_instance = RequestContext(request))

@login_required
def addviz(request,project):    
    project = get_object_or_404(Project, slug = project)
    if project.creator != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = VisualizationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("../")
    else:
        form = VisualizationForm()
    form.fields['dataset'].queryset = Dataset.objects.filter(project = project).exclude(openspending__isnull=True).exclude(openspending__exact='')
    c = { "project": project,
        "form" : form,
        "page": "viz" }
    return render_to_response("bdpsite/addviz.html", c,
        context_instance = RequestContext(request))

@login_required
def deleteviz(request,project,id):
    viz= get_object_or_404(Visualization,id = id, dataset__project__slug = project)
    if viz.dataset.project.creator != request.user:
        return HttpResponseForbidden()
    viz.delete()    
    return HttpResponseRedirect("../../")

def project(request,project):
    project = get_object_or_404(Project, slug = project)
    visualizations = Visualization.objects.raw("""
        select id from bdpsite_visualization where dataset_id in
            (select id from bdpsite_dataset where project_id =
                %s) ORDER BY 'order';"""%project.id)
    c = {"project": project,
         "visualizations": visualizations}
    return render_to_response("bdpsite/project.html", c,
        context_instance = RequestContext(request))

def userview_project(request,project):
    project = get_object_or_404(Project, slug = project)
    c = {"project": project}
    if project.featured_viz:
        c.update({"featured_dataset": project.featured_viz.dataset.name})
    return render_to_response("bdpsite/viewer_project.html", c,
        context_instance = RequestContext(request))

def userview_dataset_index(request,project):
    project = get_object_or_404(Project, slug = project)
    datasets = Dataset.objects.filter(project = project)
    c={"project": project,
       "datasets": datasets,
       "page": "datasets" }
    return render_to_response("bdpsite/viewer_dataset_index.html", c,
        context_instance = RequestContext(request))

def userview_dataset(request,project,dataset):
    project = get_object_or_404(Project, slug = project)
    dataset = get_object_or_404(Dataset, name = dataset, project = project)
    visualizations = Visualization.objects.filter(dataset__id = dataset.id)
    c={"project": project,
        "dataset": dataset,
        "visualizations": visualizations,
        "page": "dataset"}
    return render_to_response("bdpsite/viewer_dataset.html", c,
        context_instance = RequestContext(request))