from django.conf.urls import patterns, include, url
from django.contrib import admin

from tastypie.api import Api
from backend.api import *

v1_api = Api(api_name='v1')

v1_api.register(WorkingBoundaryResource())
v1_api.register(FarmResource())
v1_api.register(JobResource())
v1_api.register(WaypointResource())
v1_api.register(TractorResource())
v1_api.register(RunningJobResource())
v1_api.register(CompletedPointResource())

from .views import (FarmPanelView, HomeView, RegistrationView, RegistrationCompleteView)
admin.autodiscover()


urlpatterns = patterns(
	'',
    url(
        regex=r'^$',
        view=HomeView.as_view(),
        name='home',
    ),
    url(
        regex=r'^account/logout/$',
        view='django.contrib.auth.views.logout',
        name='logout',
    ),
    url(
        regex=r'^panel/$',
        view=FarmPanelView.as_view(),
        name='panel',
    ),
    url(
        regex=r'^account/register/$',
        view=RegistrationView.as_view(),
        name='registration',
    ),
    url(
        regex=r'^account/register/done/$',
        view=RegistrationCompleteView.as_view(),
        name='registration_complete',
    ),
    url(r'', include('two_factor.urls', 'two_factor')),
    url(r'', include('user_sessions.urls', 'user_sessions')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
)
