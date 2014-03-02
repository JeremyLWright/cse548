from tastypie.resources import ModelResource
from .models import Tractor
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization

class TractorResource(ModelResource):
    class Meta:
        queryset = Tractor.objects.all()
        resource_name = 'tractor'
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
