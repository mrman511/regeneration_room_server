import datetime
timedelta = datetime.timedelta
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
    if data['duration']:
      duration=data['duration']
      if data['duration'] % 30 != 0:
        raise serializers.ValidationError('Appointments can only be made in 30 minute increments.')

    # validate date
    if data['date']:
      date=data['date']
      datetime.datetime
      day_num=date.weekday()
      day_name=date.strftime('%A')
      # check if open for the day of the week for the given date
      if not hours.weekdays_open[day_num]:
        raise serializers.ValidationError(f'Unfortunately, Regeneration Room is not open on {day_name}s')

      operating_hours={
        'opening_hours': hours.opening_hours[day_num],
        'closing_hours': hours.closing_hours[day_num],
      }

      # if requested appointment date is a holiday, check if open on day
      try:
        holiday = HolidayHours.objects.filter(operating_hours=hours.id, date=date)[0]
      except:
        holiday = None

      if isinstance(holiday, HolidayHours):
        if not holiday.is_open:
          msg = holiday.name if holiday.name else f'the day {date}'
          raise serializers.ValidationError(f'Unfortunatly we are not open for {msg}.')

        # change operating hours to day specific hours
        operating_hours['opening_hours']=holiday.opening_hours
        operating_hours['closing_hours']=holiday.closing_hours
          

    # validate time
    if data['time']:
      time=data['time']
      # convert datetime.time to datetime.datetime
      def convert_time(time):
        return datetime.datetime.strptime(str(time), hours.TIME_FORMAT)

      # if time is before operating_hours['opening_hours']
      if time < operating_hours['opening_hours']:
        raise serializers.ValidationError(f'Earliest available booking time for Regeneration Room on { date } is { operating_hours["opening_hours"] }')
      
      # if time + duration is after operating_hours['closing_hours']
      if (convert_time(time) + timedelta(minutes=duration)) > convert_time(operating_hours['closing_hours']):
        raise serializers.ValidationError(f'Latest available booking time for Regeneration Room on { date } is { operating_hours["closing_hours"] }')
     
      if (not time.minute==0 and not time.minute==30):
        # minutes = time.minute
        # converted_time = convert_time(time)
        # minutes = 

        raise serializers.ValidationError('Appoinments at Regeneration Room are begin every half hour ')
    return data

  def create(self, validated_data):
    appointment=Appointment.objects.create(
      duration=validated_data['duration'],
      user=validated_data['user']
    )
    appointment.save()
    return validated_data