from django.conf.urls import patterns, include, url
from django.contrib import admin
from tdd import views
import tdd.urls
from django.conf import settings
from django.conf.urls.static import static
from blog.views import home, about, contact, input_view, add_workspace, remove_workspace, username

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^about$', about, name='about'),
    url(r'^contact$', contact, name='contact'),
    url(r'^input/', input_view, name='input_view'),
    url(r'^add/workspace/', add_workspace, name='add_workspace'),
    url(r'^remove/workspace/', remove_workspace, name='remove_workspace'),
    url(r'^username/', username, name='username'),
    url(r'^tdd/', views.HomeView.as_view(), name='home_view'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(tdd.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
