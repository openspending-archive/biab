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
    url(r'^user/new/$', 'bdpsite.views.createuser'),
    url(r'^user/login/$', 'bdpsite.views.login'),
    url(r'^user/logout/$', 'bdpsite.views.logout'),
    url(r'^user/(?P<user>[-\w]+)/$', 'bdpsite.views.profile'),
    url(r'^create/$', 'bdpsite.views.create'),
    url(r'^createbare/$', 'bdpsite.views.createbare'),
    url(r'^(?P<project>[-\w]+)/edit/$',
        'bdpsite.views.editproject'),
    url(r'^(?P<project>[-\w]+)/packages/$',
        'bdpsite.views.packages'),
    url(r'^(?P<project>[-\w]+)/packages/add/$',
        'bdpsite.views.addpackage'),
    url(r'^(?P<project>[-\w]+)/packages/package/(?P<package>[-\w]+)$',
        'bdpsite.views.package'),
#    url(r'^(?P<project>[-\w]+)/packages/add/$',
#        'bdpsite.views.addpackage'),
    url(r'^(?P<project>[-\w]+)/datasets/$',
        'bdpsite.views.datasets'),
    url(r'^(?P<project>[-\w]+)/visualize/$',
        'bdpsite.views.visualizations'),
    url(r'^(?P<project>[-\w]+)/datasets/add/$',
        'bdpsite.views.adddataset'),
    url(r'^(?P<project>[-\w]+)/visualize/add/$',
        'bdpsite.views.addviz'),
    url(r'^(?P<project>[-\w]+)/datasets/delete/(?P<id>\d+)/$',
        'bdpsite.views.deletedataset'),
    url(r'^(?P<project>[-\w]+)/visualize/delete/(?P<id>\d+)/$',
        'bdpsite.views.deleteviz'),
    url(r'^(?P<project>[-\w]+)/$',
        'bdpsite.views.project'),
)
