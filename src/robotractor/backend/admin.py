from django.contrib import admin
from models import Farm, Tractor

class FarmAdmin(admin.ModelAdmin):
    pass
admin.site.register(Farm, FarmAdmin)

class TractorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Tractor, TractorAdmin)

# Register your models here.
