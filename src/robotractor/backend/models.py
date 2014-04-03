from django.db import models
from django.conf import settings
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

class Job(models.Model):
    name = models.CharField(max_length=200)
    boundary = models.ForeignKey(WorkingBoundary)
    created_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.name

class Waypoint(models.Model):
    lat = models.FloatField()
    longitude = models.FloatField()
    sort_order = models.IntegerField()
    job = models.ForeignKey(Job)
    def __unicode__(self):
        return "[{0}.{1}] {2}N x {3}W".format(self.job, self.sort_order, self.lat, self.longitude)


class Tractor(models.Model):
    farm = models.ForeignKey(Farm)
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()
    public_key = models.FileField(upload_to='keys')
    jabberid = models.EmailField(max_length=254)
    def __unicode__(self):
        return self.name

class RunningJob(models.Model):
    last_checkin_time = models.DateTimeField(auto_now=True)
    last_update_time = models.DateTimeField(auto_now=True)
    active = models.BooleanField()
    tractor = models.ForeignKey(Tractor)
    job = models.ForeignKey(Job)
    def __unicode__(self):
        return "{0}/{1}".format(self.job, self.tractor)

class CompletedPoint(models.Model):
    lat = models.FloatField()
    longitude = models.FloatField()
    update_time = models.DateTimeField(auto_now=True)
    active_job = models.ForeignKey(RunningJob)
    def __unicode__(self):
        return "[{0}] {1}N x {2}W @ {3}".format(self.active_job, self.lat, self.longitude, self.update_time)
