from django.contrib import admin
from .models import Operations, OperatingHours, HolidayHours

# Register your models here.
admin.site.register(Operations)
admin.site.register(OperatingHours)
admin.site.register(HolidayHours)