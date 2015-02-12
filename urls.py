from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'djangoblog.blog.views.home', name='home'),

     url(r'^about$', 'djangoblog.blog.views.about', name='about'),

     url(r'^contact$', 'djangoblog.blog.views.contact', name='contact'),

     url(r'^input/', 'djangoblog.blog.views.input', name='input'),

     url(r'^hoj/', 'djangoblog.blog.views.hoj', name='hoj'),

     url(r'^username/', 'djangoblog.blog.views.username', name='username'),
    # url(r'^FirstBlog/', include('FirstBlog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
