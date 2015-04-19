from django.conf.urls import patterns, include, url
from django.contrib import admin
from tdd import views
import tdd.urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'blog.views.home', name='home'),

    url(r'^about$', 'blog.views.about', name='about'),

    url(r'^contact$', 'blog.views.contact', name='contact'),

    url(r'^input/', 'blog.views.input_view', name='input_view'),

    url(r'^add/workspace/', 'blog.views.add_workspace', name='add_workspace'),

    url(r'^remove/workspace/', 'blog.views.remove_workspace', name='remove_workspace'),

    url(r'^username/', 'blog.views.username', name='username'),

    url(r'^tdd/', views.HomeView.as_view(), name='home_view'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include(tdd.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)