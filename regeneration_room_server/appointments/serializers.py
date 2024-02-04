from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):

  class Meta:
    model=Appointment
    fields='__all__'
    read_only_fields=['id', 'created', 'last_updated']

  def validate(self, data):
    # duration needs to be a multiple of 30
    if data['duration'] and data['duration'] % 30 != 0:
      raise serializers.ValidationError('Appointments can only be made in 30 minute increments.')
    return data

  def create(self, validated_data):
    appointment=Appointment.objects.create(
      duration=validated_data['duration'],
      user=validated_data['user']
    )
    appointment.save()
    return validated_data