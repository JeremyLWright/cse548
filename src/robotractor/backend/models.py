from django.db import models

class Tractor(models.Model):
	name = models.CharField(max_length=100)
	