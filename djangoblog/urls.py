from django.conf.urls import patterns, include, url
from django.contrib import admin
from tdd import views
import tdd.urls

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'blog.views.home', name='home'),

    url(r'^about$', 'blog.views.about', name='about'),

    url(r'^contact$', 'blog.views.contact', name='contact'),

    url(r'^input/', 'blog.views.input', name='input'),

    url(r'^hoj/', 'blog.views.hoj', name='hoj'),

    url(r'^add/workspace/', 'blog.views.add_workspace', name='add_workspace'),

    url(r'^remove/workspace/', 'blog.views.remove_workspace', name='remove_workspace'),

    url(r'^testform/', 'blog.views.testform', name='testform'),

    url(r'^testloop/', 'blog.views.testloop', name='testloop'),

    url(r'^username/', 'blog.views.username', name='username'),

    url(r'^tdd/', views.HomeView.as_view(), name='home_view'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include(tdd.urls)),
)