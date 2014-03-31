from django.contrib import admin
from .models import Tractor, Farm, WorkingBoundary, Waypoint, Job, RunningJob

class TractorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Tractor, TractorAdmin)

class FarmAdmin(admin.ModelAdmin):
    pass
admin.site.register(Farm, FarmAdmin)

class WorkingBoundaryAdmin(admin.ModelAdmin):
    pass
admin.site.register(WorkingBoundary, WorkingBoundaryAdmin)

class WaypointAdmin(admin.ModelAdmin):
    pass
admin.site.register(Waypoint, WaypointAdmin)

class JobAdmin(admin.ModelAdmin):
    pass
admin.site.register(Job, JobAdmin)

class RunningJobAdmin(admin.ModelAdmin):
    pass
admin.site.register(RunningJob, RunningJobAdmin)
# Register your models here.
