from django.db import models
from django.contrib.auth.models import User

class Farm(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name
    
class Tractor(models.Model):
    name = models.CharField(max_length=200)
    operator = models.ForeignKey(User)
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()
    farm = models.ForeignKey(Farm)
    def __unicode__(self):
        return "{0} @ {1},{2},{3} driven by {4}".format(self.name, self.latitude, self.longitude, self.altitude, self.operator)



    
	
