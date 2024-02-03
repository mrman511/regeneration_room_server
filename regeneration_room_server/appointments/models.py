import uuid
from datetime import date, time
from django.utils import timezone
import time
from django.db import models
from users.models import CustomUser

# Create your models here.
class Appointment(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user=models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.PROTECT)
  date = models.DateField(blank=True, null=True)
  time = models.TimeField(default='09:00')
  duration=models.IntegerField(default=60, help_text='Duration in minutes')
  created = models.DateTimeField(auto_now_add=True)
  last_updated=models.DateTimeField(auto_now=True)