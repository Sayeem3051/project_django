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
]