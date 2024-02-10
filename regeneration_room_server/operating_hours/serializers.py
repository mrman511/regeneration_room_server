from rest_framework import serializers
from operating_hours.models import Operations, OperatingHours, HolidayHours
from operating_hours.default_models import hours, operations
import datetime
timedelta = datetime.timedelta


import pprint
pprint = pprint.PrettyPrinter(indent=4).pprint


class OperationsSerailizer(serializers.ModelSerializer):
  class Meta:
    model=Operations
    fields="__all__"

class HolidayHoursSerializer(serializers.ModelSerializer):
  class Meta:
    model=HolidayHours
    fields="__all__"

  def convert_date(self, date):
    return datetime.datetime.strptime(str(date), hours.DATE_FORMAT).date()
  def convert_time(self, time):
    return datetime.datetime.strptime(str(time), hours.TIME_FORMAT)

  # validate for presence of required fields
  # as well as fields that correspond with other fields
  def validate(self, data):
    # date is a required field
    if not hasattr(self, 'instance'):
      try:
        date=data['date']
      except: 
        raise serializers.ValidationError('A date is required for holiday hours')

    # is is_open not supplied set is open to False
    try:
      is_open=data['is_open']
    except:
      data['is_open']=False

    # if is_open validate for opening and closing hours
    if data['is_open']:
      try:
        opening_hours=data['opening_hours']
        closing_hours=data['closing_hours']
        if opening_hours >= closing_hours:
          raise serializers.ValidationError('Selected closing hours cannot be before selected opening hours')
      except:
        raise serializers.ValidationError('Holiday is set to open but opening or closing hours were not provided')
    
    return data

  def validate_date(self, date):
    # only one holiday per date
    if HolidayHours.objects.filter(date=date).exists():
      raise serializers.ValidationError(f'Holiday hours already exist for {date}.')

    # ensure date after current date
    holiday_date = self.convert_date(date)
    today=datetime.datetime.now().date()
    if holiday_date <= today:
      raise serializers.ValidationError('Unable to set holidays for past dates.')

    return date

  def update(self, instance, validated_data):
    for key in validated_data.keys():
      if key == 'name':
        instance.name = validated_data['name']
      if key == 'date':
        instance.date = validated_data['date']
      if key == 'opening_hours':
        instance.opening_hours = validated_data['opening_hours']
      if key == 'closing_hours':
        instance.closing_hours = validated_data['closing_hours']
      if key == 'is_open':
        instance.is_open = validated_data['is_open']
    instance.save()
    return instance

  def create(self, validated_data):
    holiday=HolidayHours.objects.create(**validated_data)
    holiday.save()

    return validated_data

class OperatingHoursSerializer(serializers.ModelSerializer):
  holiday_hours=HolidayHoursSerializer(many=True)

  opening_hours=serializers.ListField(child=serializers.TimeField())
  closing_hours=serializers.ListField(child=serializers.TimeField())
  days_closed=serializers.ListField(child=serializers.DateField())
  class Meta:
    model=OperatingHours
    fields=['days_closed', 'opening_hours', 'closing_hours', 'weekdays_open', 'holiday_hours']
