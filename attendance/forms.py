from django import forms
from .models import Attendance
from django.contrib.auth.models import User

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['notes']

class ManualAttendanceForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    check_in_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    check_out_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    is_present = forms.BooleanField(initial=True, required=False)
    notes = forms.CharField(widget=forms.Textarea, required=False)

class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)