from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('blog.views',
    # Examples:
    url(r'^$', 'home', name='home'),

    url(r'^about$', 'about', name='about'),

    url(r'^contact$', 'contact', name='contact'),

    url(r'^input/', 'input', name='input'),

    url(r'^hoj/', 'hoj', name='hoj'),

    url(r'^add/workspace/', 'add_workspace', name='add_workspace'),

    url(r'^remove/workspace/', 'remove_workspace', name='remove_workspace'),

    url(r'^testform/', 'testform', name='testform'),

    url(r'^testloop/', 'testloop', name='testloop'),

    url(r'^username/', 'username', name='username'),

    url(r'^admin/', include(admin.site.urls)),
)