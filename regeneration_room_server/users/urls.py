from django.urls import path
from . import views

urlpatterns = [
  path('template_viewer/', views.view_template, name='view_template')
]