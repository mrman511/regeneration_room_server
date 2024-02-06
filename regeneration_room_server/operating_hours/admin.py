from django.contrib import admin
from .models import OperatingHours, HolidayHours

# Register your models here.
admin.site.register(OperatingHours)
admin.site.register(HolidayHours)