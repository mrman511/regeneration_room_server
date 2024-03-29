from django.db import models
from django.contrib.postgres.fields import ArrayField

class Operations(models.Model):
  name=models.CharField(max_length=30, unique=True)
  num_chairs=models.IntegerField(default=5)

  def __str__(self):
    return self.name


class OperatingHours(models.Model):
  TIME_FORMAT = '%H:%M:%S'
  DATE_FORMAT = '%Y-%m-%d'

  DAYS = [
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday')
  ]

  def default_days_open():
    arr = [True for i in range(5)] + [False, False]
    return arr
  def default_opening_hours():
    return ['09:00' for i in range(5)]
  def default_closing_hours():
    return ['17:00' for i in range(5)]

  opening_hours=ArrayField(models.TimeField(null=True, blank=True), size=7, default=default_opening_hours)
  closing_hours=ArrayField(models.TimeField(null=True, blank=True), size=7, default=default_closing_hours)
  days_closed=ArrayField(models.DateField(null=True, blank=True), null=True, blank=True)
  weekdays_open=ArrayField(models.BooleanField(default=True), size=7, default=default_days_open)


from .default_models import hours, operations

class HolidayHours(models.Model):
  HOURS_FORMAT = '%H:%M'
  DATE_FORMAT = '%Y-%m-%d'

  operating_hours=models.ForeignKey(OperatingHours, related_name='holiday_hours', default=hours.id, on_delete=models.CASCADE)
  name=models.CharField(null=True, blank=True, max_length=50)
  date=models.DateField(null=True, blank=True)
  opening_hours=models.TimeField(null=True, blank=True)
  closing_hours=models.TimeField(null=True, blank=True)
  is_open=models.BooleanField(default=True)

  def __eq__(self, date) -> bool:
    return self.date == date

  def __hash__(self):
    return hash(self.date)

  def __str__(self):
    return f"{self.name}: {self.date}"