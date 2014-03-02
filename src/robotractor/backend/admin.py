from django.contrib import admin
from .models import Tractor, Farm, WorkingBoundary

class TractorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Tractor, TractorAdmin)

class FarmAdmin(admin.ModelAdmin):
    pass
admin.site.register(Farm, FarmAdmin)

class WorkingBoundaryAdmin(admin.ModelAdmin):
    pass
admin.site.register(WorkingBoundary, WorkingBoundaryAdmin)


# Register your models here.
