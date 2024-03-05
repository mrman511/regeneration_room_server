from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from operating_hours.models import hours, operations
from operating_hours.serializers import OperatingHoursSerializer, OperationsSerailizer

from operating_hours.serializers import HolidayHoursSerializer
from operating_hours.models import HolidayHours

@api_view(['GET', 'PATCH', 'POST', 'DELETE'])
# @permission_classes([IsAdminUser])
def holiday_hours(request, pk=None):

  if request.method == 'POST':
    serializer=HolidayHoursSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response(status.HTTP_201_CREATED)

  if request.method == 'PATCH':
    holiday=HolidayHours.objects.get(id=pk)
    serializer=HolidayHoursSerializer(holiday, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response(status.HTTP_202_ACCEPTED)

  if request.method == 'DELETE':
    holiday=HolidayHours.objects.get(pk)
    holiday.delete()
    return Response({'detail': 'Holiday successfully deleted.'}, status.HTTP_204_NO_CONTENT)
    
  holidays=HolidayHours.objects.all()
  serializer=HolidayHoursSerializer(holidays, many=True)
  return Response(serializer.data)

@api_view(['GET', 'PATCH'])
# @permission_classes([IsAdminUser])
def store_operations(request):
  if request.method == "PATCH":
    serializer=OperationsSerailizer(operations, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response(status.HTTP_202_ACCEPTED)

  serializer=OperationsSerailizer(operations, many=False)
  return Response(serializer.data)