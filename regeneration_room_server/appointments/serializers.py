import datetime
from xml.dom import ValidationErr

from rest_framework import serializers
from .models import Appointment
from operating_hours.models import hours, HolidayHours

class AppointmentSerializer(serializers.ModelSerializer):

  class Meta:
    model=Appointment
    fields='__all__'
    read_only_fields=['id', 'created', 'last_updated']

  def validate(self, data):
    duration=60
    # duration needs to be a multiple of 30
    if data['duration'] and data['duration'] % 30 != 0:
      duration=data[duration]
      raise serializers.ValidationError('Appointments can only be made in 30 minute increments.')

    # validate date
    if data['date']:
      date=data['date']
      datetime.datetime
      day_num=date.weekday()
      day_name = date.strftime('%A')
      # check if open for the day of the week for the given date
      if not hours.weekdays_open[day_num]:
        raise serializers.ValidationError(f'Unfortunately, Regeneration Room is not open on {day_name}s')

      day={
        'date': date,
        'opening_hours': hours.opening_hours[day_num],
        'closing_hours': hours.opening_hours[day_num],
      }
      # if requested appointment date is a 
      holiday = HolidayHours.objects.filter(operating_hours=hours.id, date=date)[0]
      if isinstance(holiday, HolidayHours):
        day=holiday
        if not holiday.is_open:
          msg = holiday.name if holiday.name else f'the day {date}'
          raise serializers.ValidationError(f'Unfortunatly we are not open for {msg}.')

      # validate time
      # if data['time']
      
     
    return data

  def create(self, validated_data):
    appointment=Appointment.objects.create(
      duration=validated_data['duration'],
      user=validated_data['user']
    )
    appointment.save()
    return validated_data