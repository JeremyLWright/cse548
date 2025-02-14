from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from .models import *
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie import fields

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        allowed_methods = ['get']

class WorkingBoundaryResource(ModelResource): 
    class Meta:
        queryset = WorkingBoundary.objects.all()
        resource_name = 'workingboundary'
        authentication = SessionAuthentication()
        authorization = Authorization()
        filtering = {
                "name": ALL_WITH_RELATIONS
                }

class FarmResource(ModelResource):
    class Meta:
        queryset = Farm.objects.all()
        resource_name = 'farm'
        authentication = SessionAuthentication()
        authorization = Authorization()

class JobResource(ModelResource):
    boundary = fields.ForeignKey(WorkingBoundaryResource, 'boundary')
    user = fields.ForeignKey(UserResource, 'user')
    class Meta:
        queryset = Job.objects.all()
        resource_name = 'job'
        authentication = SessionAuthentication()
        authorization = Authorization()
        filtering = {
                "id": ALL_WITH_RELATIONS
                }

class WaypointResource(ModelResource):
    job = fields.ForeignKey(JobResource, 'job')
    class Meta:
        queryset = Waypoint.objects.all()
        resource_name = 'waypoint'
        authentication = SessionAuthentication()
        authorization = Authorization()
        filtering = {
                "job": ALL_WITH_RELATIONS
                }

class TractorResource(ModelResource):
    class Meta:
        queryset = Tractor.objects.all()
        resource_name = 'tractor'
        authentication = SessionAuthentication()
        authorization = Authorization()

class RunningJobResource(ModelResource):
    job = fields.ForeignKey(JobResource, 'job')
    tractor = fields.ForeignKey(TractorResource, 'tractor')
    class Meta:
        queryset = RunningJob.objects.all()
        resource_name = 'runningjob'
        authentication = SessionAuthentication()
        authorization = Authorization()

class CompletedPointResource(ModelResource):
    active_job = fields.ForeignKey(RunningJobResource, 'active_job')
    class Meta:
        queryset = CompletedPoint.objects.all()
        resource_name = 'completedpoint'
        authentication = SessionAuthentication()
        authorization = Authorization()
        filtering = {
                "id": ALL_WITH_RELATIONS,
                "active_job": ALL_WITH_RELATIONS
                }

