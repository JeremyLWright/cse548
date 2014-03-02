from django.db import models
from django.contrib.auth.models import User

class WorkingBoundary(models.Model):
    name = models.CharField(max_length=200)
    nw_lat = models.FloatField()
    nw_long = models.FloatField()
    se_lat = models.FloatField()
    se_long = models.FloatField()

    def __unicode__(self):
        return "{0} at {1}N {2}W by {3}N {4}W".format(self.name, self.nw_lat, self.nw_long, self.se_lat, self.se_long)

class Farm(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return self.name


class Tractor(models.Model):
    owner = models.ForeignKey(Farm)
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()
    def __unicode__(self):
        return self.name

	
