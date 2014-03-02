from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.contrib import admin

from tastypie.api import Api
from backend.api import TractorResource

v1_api = Api(api_name='v1')
v1_api.register(TractorResource())

from .views import (ExampleSecretView, HomeView, RegistrationView,
                    RegistrationCompleteView)
admin.autodiscover()

LOGIN_URL=reverse_lazy('two_factor:login')
LOGIN_REDIRECT_URL=reverse_lazy('two_factor:profile')

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
        regex=r'^secret/$',
        view=ExampleSecretView.as_view(),
        name='secret',
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
