from tastypie.resources import ModelResource
from .models import Tractor, Job, Waypoint, CompletedPoint
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization

class TractorResource(ModelResource):
    class Meta:
        queryset = Tractor.objects.all()
        resource_name = 'tractor'
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()

class JobResource(ModelResource):
    class Meta:
        queryset = Job.objects.all()
        resource_name = 'job'
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()

class WaypointResource(ModelResource):
    class Meta:
        queryset = Waypoint.objects.all()
        resource_name = 'waypoint'
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()

class CompletedPointResource(ModelResource):
    class Meta:
        queryset = CompletedPoint.objects.all()
        resource_name = 'completedpoint'
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
