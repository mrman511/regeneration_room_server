from rest_framework import serializers
from .models import Appointment
from users.serializers import UserViewSerializer

class AppointmentSerializer(serializers.ModelSerializer):
  user = UserViewSerializer(many=False, read_only=True)

  class Meta:
    model=Appointment
    # fields='__all__'
    exclude=['id',]
    read_only_fields=['id', 'created', 'last_updated']

  def validate(self, data):
    # duration needs to be a multiple of 30
    if data['duration'] and data['duration'] % 30 != 0:
      raise serializers.ValidationError('Appointments can only be made in 30 minute increments')
    
    appointment=Appointment.objects.create()
    appointment.duration=data['duration']
    appointment.user=data['user']
    appointment.save()
    return data