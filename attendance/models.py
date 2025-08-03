from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Attendance(models.Model):
    ATTENDANCE_TYPES = (
        ('face', 'Face Recognition'),
        ('fingerprint', 'Fingerprint'),
        ('manual', 'Manual Entry'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    attendance_type = models.CharField(max_length=20, choices=ATTENDANCE_TYPES, default='manual')
    is_present = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date', 'user']
    
    def __str__(self):
        return f"{self.user.username} - {self.date}"
    
    def get_duration(self):
        if self.check_in_time and self.check_out_time:
            duration = self.check_out_time - self.check_in_time
            hours = duration.seconds // 3600
            minutes = (duration.seconds % 3600) // 60
            return f"{hours}h {minutes}m"
        return "N/A"
        
    def get_duration_hours(self):
        """Return duration in decimal hours for calculations"""
        if self.check_in_time and self.check_out_time:
            duration = self.check_out_time - self.check_in_time
            hours = duration.seconds / 3600  # Decimal hours
            return round(hours, 2)
        return 0

class AttendanceLog(models.Model):
    LOG_TYPES = (
        ('check_in', 'Check In'),
        ('check_out', 'Check Out'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    log_type = models.CharField(max_length=10, choices=LOG_TYPES)
    verification_method = models.CharField(max_length=20, choices=Attendance.ATTENDANCE_TYPES)
    success = models.BooleanField(default=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    device_info = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.log_type} - {self.timestamp}"
