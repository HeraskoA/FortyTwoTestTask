from django.conf.urls import patterns, include, url
from hello import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'fortytwo_test_task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.home, name='home'),
    url(r'^requests/', views.requests, name='requests'),
    url(r'^admin/', include(admin.site.urls)),
)
