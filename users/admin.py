from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'department', 'position', 'date_joined')
    search_fields = ('user__username', 'user__email', 'employee_id', 'department')
    list_filter = ('department', 'date_joined')
    readonly_fields = ('date_joined',)
