from django.conf.urls import patterns, include, url
from hello import views
from django.contrib import admin
from .settings.common import MEDIA_ROOT
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'fortytwo_test_task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.home, name='home'),
    url(r'^requests/$', views.requests, name='requests'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^edit/(?P<pk>\d+)/', views.Edit.as_view(), name='edit'),
    url(
        r'^users/logout/$',
        auth_views.logout,
        kwargs={'next_page': 'home'},
        name='auth_logout'
    ),
    url(
        r'^register/complete/$',
        RedirectView.as_view(pattern_name='home'),
        name='registration_complete'
    ),
    url(r'^users/',
        include('registration.backends.simple.urls', namespace='users')
        ),
)
urlpatterns += patterns(
    '',
    url(
        r'^uploads/(?P<path>.*)/$',
        'django.views.static.serve',
        {'document_root': MEDIA_ROOT}
        )
    )
