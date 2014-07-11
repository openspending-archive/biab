from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'biab.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # for development
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'bdpsite.views.welcome'),
    url(r'^help/$',
        'bdpsite.views.help'),
    url(r'^projects/$',
        'bdpsite.views.projects'),

    url(r'^user/new/$', 'bdpsite.views.createuser'),
    url(r'^user/login/$', 'bdpsite.views.login'),
    url(r'^user/logout/$', 'bdpsite.views.logout'),
    url(r'^user/(?P<user>[-\w]+)/$', 'bdpsite.views.profile'),

    url(r'^project/create/$', 'bdpsite.views.create'),
    url(r'^project/createbare/$', 'bdpsite.views.createbare'),

#    url(r'^project/(?P<project>[-\w]+)/$',
#        'bdpsite.views.project'),
    url(r'^project/(?P<project>[-\w]+)/$',
        'bdpsite.views.editproject'),
    url(r'^project/(?P<project>[-\w]+)/packages/$',
        'bdpsite.views.packages'),
    url(r'^project/(?P<project>[-\w]+)/packages/add/$',
        'bdpsite.views.addpackage'),
    url(r'^project/(?P<project>[-\w]+)/packages/edit/(?P<package>[-\w]+)/$',
        'bdpsite.views.package'),
    url(r'^project/(?P<project>[-\w]+)/packages/delete/(?P<id>\d+)/$',
        'bdpsite.views.deletepackage'),
#    url(r'^(?P<project>[-\w]+)/packages/add/$',
#        'bdpsite.views.addpackage'),
    url(r'^project/(?P<project>[-\w]+)/datasets/$',
        'bdpsite.views.datasets'),
    url(r'^project/(?P<project>[-\w]+)/datasets/(?P<id>\d+)/$',
        'bdpsite.views.dataset'),
    url(r'^project/(?P<project>[-\w]+)/visualize/$',
        'bdpsite.views.visualizations'),
    url(r'^project/(?P<project>[-\w]+)/datasets/add/$',
        'bdpsite.views.adddataset'),
    url(r'^project/(?P<project>[-\w]+)/visualize/add/$',
        'bdpsite.views.addviz'),
    url(r'^project/(?P<project>[-\w]+)/datasets/delete/(?P<id>\d+)/$',
        'bdpsite.views.deletedataset'),
    url(r'^project/(?P<project>[-\w]+)/datasets/preprocess/(?P<id>\d+)/$',
        'bdpsite.views.preprocessdataset'),
    url(r'^project/(?P<project>[-\w]+)/datasets/model/(?P<id>\d+)/$',
        'bdpsite.views.generatemodel'),
    url(r'^project/(?P<project>[-\w]+)/datasets/os-upload/(?P<id>\d+)/$',
        'bdpsite.views.osuploaddataset'),
    url(r'^project/(?P<project>[-\w]+)/visualize/delete/(?P<id>\d+)/$',
        'bdpsite.views.deleteviz'),
    
    url(r'^openspending/(?P<id>\d+)/$',
        'bdpsite.views.get_openspending'),

    url(r'^(?P<project>[-\w]+)/$',
        'bdpsite.views.userview_project'),
    url(r'^(?P<project>[-\w]+)/datasets/$',
        'bdpsite.views.userview_dataset_index'),
    url(r'^(?P<project>[-\w]+)/(?P<dataset>[-\w]+)/$',
        'bdpsite.views.userview_dataset'),
)
