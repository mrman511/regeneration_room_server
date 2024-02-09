from django.urls import path, include
from . import views

from rest_framework_simplejwt.views import (
  TokenObtainPairView,
  TokenRefreshView,
)

urlpatterns = [
  path('', views.end_points),

  path('users/', views.users),
  path('users/reset_password/', views.reset_password),
  path('users/reset_password/<str:encoded_pk>/<str:token>/', views.reset_password),
  path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

  path('appointments/', views.appointments),
  path('appointments/<str:pk>/', views.appointments),

  path('operating_hours/', views.operating_hours),

  # admin routes
  path('admin/holiday_hours/', views.holiday_hours),
]