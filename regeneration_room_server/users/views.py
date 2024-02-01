from django.shortcuts import render
from django.conf import settings
import environ
env = environ.Env()

def view_template(request):
  context = {
    'url': settings.CLIENT_PATH,
    'logo_url': env('HOST_URL') + '/static/images/logos/regeneration-room-full.png'
    }
  return render(request, "email_templates/reset_password.html", context)
