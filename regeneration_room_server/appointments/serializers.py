import datetime
timedelta = datetime.timedelta
from itertools import chain
from rest_framework import serializers
from .models import Appointment
from operating_hours.models import HolidayHours
from operating_hours.default_models import hours, operations
import pprint
pprint = pprint.PrettyPrinter(indent=4).pprint


class AppointmentSerializer(serializers.ModelSerializer):

  class Meta:
    model=Appointment
    fields='__all__'
    read_only_fields=['id', 'created', 'last_updated']

  def validate(self, data):
    duration=60
    instance = self.instance if self.instance else None
    # convert date to datetime.datetime
    def convert_date(date):
      return datetime.datetime.strptime(str(date), hours.DATE_FORMAT).date()
    # convert datetime.time to datetime.datetime
    def convert_time(time):
      return datetime.datetime.strptime(str(time), hours.TIME_FORMAT)
    # get requested date and time as datetime
    def get_appointment_datetime(date, time):
      return datetime.datetime.strptime(f'{str(date)}:{str(time)}', f'{hours.DATE_FORMAT}:{hours.TIME_FORMAT}')
      
    # validate duration
    if data['duration']:
      duration=data['duration']
      if duration < 30:
        raise serializers.validationError('Appointments need to be a minimum of 30 minutes')
      # duration needs to be a multiple of 30
      if data['duration'] % 30 != 0:
        raise serializers.ValidationError('Appointments can only be made in 30 minute increments.')

    # validate date
    try:
      date=data['date']
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
    except:
      raise serializers.ValidationError('Invalid appointment date requested.')

    # validate time
    try:
      time=data['time']

      # if time is before operating_hours['opening_hours']
      if time < operating_hours['opening_hours']:
        raise serializers.ValidationError(f'Earliest available booking time for Regeneration Room on { date } is { operating_hours["opening_hours"] }')
      
      # if time + duration is after operating_hours['closing_hours']
      if (convert_time(time) + timedelta(minutes=duration)) > convert_time(operating_hours['closing_hours']):
        raise serializers.ValidationError(f'Latest available booking time for Regeneration Room on { date } is { operating_hours["closing_hours"] }')

      # if time is not on the hour or half hour
      if (not time.minute==0 and not time.minute==30):
        raise serializers.ValidationError('Appoinments at Regeneration Room are begin every half hour')
    except: 
      raise serializers.validationError('Invalid appointment time requested.')
    
    # validate number of time slots
    requested_date=convert_date(date)
    requested_datetime=get_appointment_datetime(date, time)

    #time slots = duration of requested appointment in 30 minute increments
    requested_time_slots = [(requested_datetime + timedelta(minutes=i * 30)).time() for i in range(int(duration/30))]

    # validate for open timeslots in scedule
    for time_slot in requested_time_slots:
      # get appointments with a duration of 60 that were scheduled for previous time slot
      previous_time_slot = (requested_datetime - timedelta(minutes=30)).time()
      apps1 = Appointment.objects.filter(date=requested_date, time=previous_time_slot, duration=60)
      # get appointments for selected time slots
      apps2 = Appointment.objects.filter(date=requested_date, time=time_slot)
      # combine apps1 and apps2 appointment lists
      apps=list(chain(apps1, apps2))
      # check apps list for instance and remove if present
      if instance:
        try:
          apps.remove(instance)
        except:
          pass
      # ERROR if length of combined appoinment lists is greater then number of chairs available
      if (len(apps) >= operations.num_chairs):  
        raise serializers.ValidationError(f"Unfortunately our shedule is full for {requested_datetime.strftime('%H:%M')} on {requested_datetime.strftime('%B %d')}")
      
    return data

  def update(self, instance, validated_data):
    if validated_data['date']:
      instance.date=validated_data['date']
    if validated_data['time']:
      instance.time=validated_data['time']
    if validated_data['duration']:
      instance.duration=validated_data['duration']
    instance.save()
    return validated_data

  def create(self, validated_data):
    appointment=Appointment.objects.create(
      duration=validated_data['duration'],
      user=validated_data['user'],
      date=validated_data['date'],
      time=validated_data['time']
    )
    appointment.save()
    return validated_data