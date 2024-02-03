from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class AppPreferences(models.Model):
  MON, TUE, WED, THU, FRI, SAT, SUN, = 0, 1, 2, 3, 4, 5, 6
  
  opening_hours=ArrayField(models.TimeField(null=True, blank=True), size=7)
  closing_hours=ArrayField(models.TimeField(null=True, blank=True), size=7)
  days_closed=ArrayField(models.DateField(null=True, blank=True), null=True, blank=True)
  