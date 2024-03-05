from django.urls import path, include
from . import views
from . import admin_views

from rest_framework_simplejwt.views import (
  TokenObtainPairView,
  TokenRefreshView,
)

urlpatterns = [
  path('', views.end_points),

  path('user/', views.user),

  path('users/', views.users),
  path('users/reset_password/', views.reset_password),
  path('users/reset_password/<str:encoded_pk>/<str:token>/', views.reset_password),
  path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

  path('appointments/', views.appointments),
  path('appointments/<str:pk>/', views.appointments),

  path('operating_hours/', views.operating_hours),

  # admin routes
  path('admin/holiday_hours/', admin_views.holiday_hours),
  path('admin/holiday_hours/<str:pk>/', admin_views.holiday_hours),
  path('admin/operations/', admin_views.store_operations),
]