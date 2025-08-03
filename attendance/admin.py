from django.contrib import admin
from .models import Attendance, AttendanceLog

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'check_in_time', 'check_out_time', 'attendance_type', 'is_present', 'get_duration')
    list_filter = ('date', 'is_present', 'attendance_type')
    search_fields = ('user__username', 'user__email', 'notes')
    date_hierarchy = 'date'

@admin.register(AttendanceLog)
class AttendanceLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'log_type', 'verification_method', 'success', 'ip_address')
    list_filter = ('log_type', 'verification_method', 'success', 'timestamp')
    search_fields = ('user__username', 'user__email', 'ip_address')
    date_hierarchy = 'timestamp'
