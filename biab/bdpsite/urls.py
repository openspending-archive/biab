from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'biab.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'bdpsite.views.welcome'),
    url(r'^user/new/$', 'bdpsite.views.createuser'),
    url(r'^user/login/$', 'bdpsite.views.login'),
    url(r'^user/logout/$', 'bdpsite.views.logout'),
    url(r'^user/(?P<user>[-\w]+)/$', 'bdpsite.views.profile'),
    url(r'^create/$', 'bdpsite.views.create'),
    url(r'^(?P<project>[-\w]+)/edit/$',
        'bdpsite.views.editproject'),
)
