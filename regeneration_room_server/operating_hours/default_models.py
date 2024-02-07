from .models import Operations, OperatingHours

try:
  operations = Operations.objects.first()
except:
  operations = Operations.objects.create(name='Regeneration Room')
  operations.save()

# the base operating_hours meant to be used for the site
try:
  hours = OperatingHours.objects.first()
except:
  hours = OperatingHours.objects.create()
  hours.save()
