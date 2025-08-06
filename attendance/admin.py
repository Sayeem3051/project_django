from django.contrib import admin
from .models import Attendance, AttendanceLog, DailyAttendanceNotification, AttendanceStatus
from django.utils import timezone
from django.db.models import Q
from datetime import date

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

@admin.register(DailyAttendanceNotification)
class DailyAttendanceNotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'notification_type', 'date', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'date', 'created_at')
    search_fields = ('title', 'message')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    
    actions = ['mark_as_read', 'mark_as_unread', 'create_daily_summary']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected notifications as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected notifications as unread"
    
    def create_daily_summary(self, request, queryset):
        today = date.today()
        present_count = AttendanceStatus.objects.filter(date=today, status='present').count()
        absent_count = AttendanceStatus.objects.filter(date=today, status='absent').count()
        late_count = AttendanceStatus.objects.filter(date=today, status='late').count()
        
        summary_message = f"""
        Daily Attendance Summary for {today}:
        
        ✅ Present: {present_count} students
        ❌ Absent: {absent_count} students
        ⏰ Late: {late_count} students
        
        Total Students: {present_count + absent_count + late_count}
        """
        
        DailyAttendanceNotification.objects.create(
            date=today,
            notification_type='daily_summary',
            title=f'Daily Attendance Summary - {today}',
            message=summary_message
        )
        
        self.message_user(request, f"Daily summary notification created for {today}")
    create_daily_summary.short_description = "Create daily attendance summary"

@admin.register(AttendanceStatus)
class AttendanceStatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'status', 'check_in_time', 'check_out_time', 'is_notified')
    list_filter = ('status', 'date', 'is_notified')
    search_fields = ('user__username', 'user__email', 'notes')
    date_hierarchy = 'date'
    readonly_fields = ('is_notified',)
    
    actions = ['mark_all_present', 'mark_all_absent', 'send_notifications']
    
    def mark_all_present(self, request, queryset):
        queryset.update(status='present')
    mark_all_present.short_description = "Mark selected as present"
    
    def mark_all_absent(self, request, queryset):
        queryset.update(status='absent')
    mark_all_absent.short_description = "Mark selected as absent"
    
    def send_notifications(self, request, queryset):
        today = date.today()
        
        # Create notifications for absent employees
        absent_users = queryset.filter(status='absent', date=today)
        if absent_users.exists():
            absent_list = ', '.join([user.user.username for user in absent_users])
            DailyAttendanceNotification.objects.create(
                date=today,
                notification_type='absent_alert',
                title=f'Absent Students Alert - {today}',
                message=f'The following students are absent today: {absent_list}'
            )
        
        # Create notifications for late employees
        late_users = queryset.filter(status='late', date=today)
        if late_users.exists():
            late_list = ', '.join([user.user.username for user in late_users])
            DailyAttendanceNotification.objects.create(
                date=today,
                notification_type='late_alert',
                title=f'Late Students Alert - {today}',
                message=f'The following students are late today: {late_list}'
            )
        
        queryset.update(is_notified=True)
        self.message_user(request, f"Notifications sent for {queryset.count()} attendance records")
    send_notifications.short_description = "Send notifications for selected records"
