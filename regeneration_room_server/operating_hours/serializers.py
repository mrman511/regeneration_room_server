from dataclasses import fields
from rest_framework import serializers
from operating_hours.models import OperatingHours, HolidayHours


class HolidayHoursSerializer(serializers.ModelSerializer):
  class Meta:
    model=HolidayHours
    fields="__all__"

class OperatingHoursSerializer(serializers.ModelSerializer):
  holiday_hours=HolidayHoursSerializer(many=True)

  opening_hours=serializers.ListField(child=serializers.TimeField())
  closing_hours=serializers.ListField(child=serializers.TimeField())
  days_closed=serializers.ListField(child=serializers.DateField())
  class Meta:
    model=OperatingHours
    fields=['days_closed', 'opening_hours', 'closing_hours', 'weekdays_open', 'holiday_hours']
