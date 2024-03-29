from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from users.models import CustomUser
from users.serializers import CustomUserSerializer
from email_templates import welcome_template

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from users.serializers import ResetPasswordSerializer


import environ
env = environ.Env()


import pprint
pprint = pprint.PrettyPrinter(indent=4).pprint

# Create your views here.
@api_view(['GET'])
def end_points(request):
  context={
    'end_points': {
      'GET': 'api/',
    },
    'users': {
      'GET': 'users/',
      'POST': 'users/',
    },
    'appointments': {
      'GET': {
        'all': 'appointments/',
        'id': 'appointments/<str:pk>/'
      },
      'POST': 'appointments/',
      'PATCH': 'appointments/<str:pk>/',
      'DELETE': 'appointments/<str:pk/>',
    },
  }
  return Response(context)

@api_view(['GET', 'POST'])
def users(request):
  if request.method == 'POST':
    newUser = request.data.dict()
    email = newUser['email']
    first_name=newUser['first_name']
    last_name=newUser['last_name']
    notifications = True if newUser['notifications'] == 'true' else False
    # send conflict response if email is already registered
    if CustomUser.objects.filter(email=email):
      context = { 'detail': 'An account with the provided email already exists.' }
      return Response(context, status.HTTP_409_CONFLICT)
    # create new user
    user = CustomUser.objects.create_user(
      email,
      newUser['password'],
    )
    user.first_name=first_name
    user.last_name=last_name
    user.notifications=notifications
    user.save()
    # send email after user is created
    send_mail(
      welcome_template.subject,
      welcome_template.message,
      settings.EMAIL_HOST_USER,
      [user.email],
      fail_silently=False
    )
    # return successful message
    context = { 'detail': f'Successfully Registered { first_name }!' }
    return Response(context, status.HTTP_201_CREATED)
  # return all users as json response
  users = CustomUser.objects.all();
  serializer = CustomUserSerializer(users, many=True)
  return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user(request):
  if request.method == 'GET':
    user = request.user
    print(user)
    serializer=CustomUserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['POST', 'PATCH'])
def reset_password(request, encoded_pk=None, token=None):
  data = request.data.dict()
  if request.method=='PATCH':
    serializer = ResetPasswordSerializer(data=request.data, context={"kwargs": { 'encoded_pk': encoded_pk, "token": token }})
    serializer.is_valid(raise_exception=True)
    return Response({'details': 'Password reset accepted' }, status.HTTP_202_ACCEPTED)
  
  if request.method=='POST':
    # get user and encode user pk and generate password reset token
    user = CustomUser.objects.get(email=data['email'])
    encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
    token = PasswordResetTokenGenerator().make_token(user)
    # create password reset-link URL
    url = settings.CLIENT_PATH + f'/login/password_reset?pk=${ encoded_pk }&token={token}'
    logo_url = env('HOST_URL') + '/static/images/logos/regerneration-room-full.png'
    # send email
    message = render_to_string('email_templates/reset_password.html', { "url": url, 'logo_url': logo_url })
    email=EmailMessage('Reset Password', message, to=[data['email']])
    email.content_subtype='html'
    email.send()
    return Response({}, status.HTTP_200_OK)

  return Response({}, status.HTTP_200_OK)

###################
# Appointment Views
###################

from appointments.models import Appointment
from appointments.serializers import AppointmentSerializer

@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def appointments(request, pk=None):
  if request.method == 'POST':
    data=request.data
    # data['user']={'id': request.user.id}
    serializer = AppointmentSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
      serializer.save(user=request.user)
      return Response(status.HTTP_201_CREATED)

  
  def get_authorized_appointment():
    # get appointment  or error
    try:
      appointment=Appointment.objects.get(pk)
    except:
      return Response({'detail': 'Invalid appointment provided'}, status.HTTP_400_BAD_REQUEST)
    # ensure proper user for appointment 
    if not appointment.user == request.user:
      return Response(status.HTTP_401_UNAUTHORIZED)
    return appointment

  if request.method == 'PATCH':
    appointment=get_authorized_appointment()
    serializer=AppointmentSerializer(appointment, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response(status.HTTP_201_ACCEPTED)

  if request.method == 'DELETE':
    appointment=get_authorized_appointment()
    appointment.delete()
    return Response({'detail': 'Appointment successfully removed.'}, status.HTTP_204_NO_CONTENT)

  # return requested Appointment
  if pk is not None:
    try:
      appointment=Appointment.objects.get(id=pk)
      serializer=AppointmentSerializer(appointment, many=False)
      return Response(serializer.data)
    except:
      return Response({'detail': 'Invalid appointment provided'}, status.HTTP_400_BAD_REQUEST)
  # default return all appointments JSON
  appointments=Appointment.objects.all()
  serializer=AppointmentSerializer(appointments, many=True)
  return Response(serializer.data)




#######################
# App Preference Views
#######################

from operating_hours.models import hours, operations
from operating_hours.serializers import OperatingHoursSerializer, OperationsSerailizer

@api_view(['GET'])
def operating_hours(request):
  serializer=OperatingHoursSerializer(hours, many=False)
  return Response(serializer.data)

# #######################
# # ADMIN Views
# #######################

# from operating_hours.serializers import HolidayHoursSerializer
# from operating_hours.models import HolidayHours

# @api_view(['GET', 'PATCH', 'POST', 'DELETE'])
# # @permission_classes([IsAdminUser])
# def holiday_hours(request, pk=None):

#   if request.method == 'POST':
#     serializer=HolidayHoursSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#       serializer.save()
#       return Response(status.HTTP_201_CREATED)

#   if request.method == 'PATCH':
#     holiday=HolidayHours.objects.get(id=pk)
#     serializer=HolidayHoursSerializer(holiday, data=request.data, partial=True)
#     if serializer.is_valid(raise_exception=True):
#       serializer.save()
#       return Response(status.HTTP_202_ACCEPTED)

#   if request.method == 'DELETE':
#     holiday=HolidayHours.objects.get(pk)
#     holiday.delete()
#     return Response({'detail': 'Holiday successfully deleted.'}, status.HTTP_204_NO_CONTENT)
    
#   holidays=HolidayHours.objects.all()
#   serializer=HolidayHoursSerializer(holidays, many=True)
#   return Response(serializer.data)

# @api_view(['GET', 'PATCH'])
# # @permission_classes([IsAdminUser])
# def store_operations(request):
#   if request.method == "PATCH":
#     serializer=OperationsSerailizer(operations, data=request.data, partial=True)
#     if serializer.is_valid(raise_exception=True):
#       serializer.save()
#       return Response(status.HTTP_202_ACCEPTED)

#   serializer=OperationsSerailizer(operations, many=False)
#   return Response(serializer.data)