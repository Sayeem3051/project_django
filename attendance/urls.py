from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.attendance_home, name='attendance_home'),
    path('mark/', views.mark_attendance, name='mark_attendance'),
    path('history/', views.attendance_history, name='attendance_history'),
    path('report/', views.attendance_report, name='attendance_report'),
    path('upload-face/', views.upload_face, name='upload_face'),
    path('upload-fingerprint/', views.upload_fingerprint, name='upload_fingerprint'),
    path('test-camera/', views.test_camera, name='test_camera'),
    path('debug-camera/', views.debug_camera, name='debug_camera'),
    path('notifications/', views.notification_dashboard, name='notification_dashboard'),
    path('mark-status/', views.mark_attendance_status, name='mark_attendance_status'),
    path('create-notification/', views.create_daily_notification, name='create_daily_notification'),
    path('mark-notification-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
]