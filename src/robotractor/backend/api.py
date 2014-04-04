from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from .models import *
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization

class WorkingBoundaryResource(ModelResource):
    class Meta:
        queryset = WorkingBoundary.objects.all()
        resource_name = 'workingboundary'
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        filtering = {
                "name": ALL_WITH_RELATIONS
                }

class FarmResource(ModelResource):
    class Meta:
        queryset = Farm.objects.all()
        resource_name = 'farm'
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

class TractorResource(ModelResource):
    class Meta:
        queryset = Tractor.objects.all()
        resource_name = 'tractor'
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()

class RunningJobResource(ModelResource):
    class Meta:
        queryset = RunningJob.objects.all()
        resource_name = 'runningjob'
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()

class CompletedPointResource(ModelResource):
    class Meta:
        queryset = CompletedPoint.objects.all()
        resource_name = 'completedpoint'
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        filtering = {
                "id": ALL_WITH_RELATIONS,
                }
