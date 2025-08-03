from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from .models import Attendance, AttendanceLog
from .forms import AttendanceForm, ManualAttendanceForm, DateRangeForm
import datetime
import csv

@login_required
def attendance_home(request):
    """Attendance home page"""
    today = timezone.now().date()
    today_attendance = Attendance.objects.filter(user=request.user, date=today).first()
    
    context = {
        'today': today,
        'attendance': today_attendance,
    }
    
    return render(request, 'attendance/home.html', context)

@login_required
def mark_attendance(request):
    """Mark attendance view"""
    today = timezone.now().date()
    now = timezone.now()
    
    # Check if attendance record exists for today
    attendance, created = Attendance.objects.get_or_create(
        user=request.user,
        date=today,
        defaults={'check_in_time': now, 'attendance_type': 'manual'}
    )
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        verification_method = request.POST.get('verification_method', 'manual')
        
        if form.is_valid():
            # Handle face verification
            if verification_method == 'face':
                if 'face_image' in request.FILES:
                    # Use the face recognition system
                    from .face_recognition_utils import process_uploaded_image, detect_faces, extract_face_features, verify_face
                    
                    # Process the uploaded face image
                    image_array = process_uploaded_image(request.FILES['face_image'])
                    if image_array is not None:
                        # Detect faces in the image
                        face_locations = detect_faces(image_array)
                        
                        if not face_locations:
                            messages.error(request, 'No face detected in the image. Please try again.')
                            context = {
                                'form': form,
                                'attendance': attendance,
                                'created': created,
                            }
                            return render(request, 'attendance/mark_attendance.html', context)
                        
                        if len(face_locations) > 1:
                            messages.error(request, 'Multiple faces detected. Please ensure only your face is visible.')
                            context = {
                                'form': form,
                                'attendance': attendance,
                                'created': created,
                            }
                            return render(request, 'attendance/mark_attendance.html', context)
                        
                        # Extract face features
                        face_features = extract_face_features(image_array, face_locations)
                        
                        if not face_features:
                            messages.error(request, 'Could not extract facial features. Please try again.')
                            context = {
                                'form': form,
                                'attendance': attendance,
                                'created': created,
                            }
                            return render(request, 'attendance/mark_attendance.html', context)
                        
                        # Verify the face
                        is_match, confidence, message = verify_face(request.user, face_features[0])
                        
                        if is_match:
                            verification_method = 'face'
                        else:
                            messages.error(request, f'Face verification failed: {message}')
                            context = {
                                'form': form,
                                'attendance': attendance,
                                'created': created,
                                'verification_failed': True,
                                'verification_message': message
                            }
                            return render(request, 'attendance/mark_attendance.html', context)
                    else:
                        messages.error(request, 'Face verification failed. Please try again or enable face recognition in your profile.')
                        context = {
                            'form': form,
                            'attendance': attendance,
                            'created': created,
                        }
                        return render(request, 'attendance/mark_attendance.html', context)
                else:
                    messages.error(request, 'Face verification failed. Please try again.')
                    context = {
                        'form': form,
                        'attendance': attendance,
                        'created': created,
                    }
                    return render(request, 'attendance/mark_attendance.html', context)
            
            # If attendance record already exists and has check_in_time but no check_out_time
            if not created and attendance.check_in_time and not attendance.check_out_time:
                attendance.check_out_time = now
                attendance.notes = form.cleaned_data.get('notes', '')
                if verification_method == 'face':
                    attendance.attendance_type = 'face'
                attendance.save()
                
                # Create attendance log for check-out
                AttendanceLog.objects.create(
                    user=request.user,
                    log_type='check_out',
                    verification_method=verification_method,
                    ip_address=request.META.get('REMOTE_ADDR'),
                    device_info=request.META.get('HTTP_USER_AGENT', '')[:255]
                )
                
                messages.success(request, f'Check-out recorded successfully using {verification_method} verification!')
            else:
                attendance_form = form.save(commit=False)
                if verification_method == 'face':
                    attendance_form.attendance_type = 'face'
                attendance_form.save()
                
                # Create attendance log for check-in if this is a new record
                if created:
                    AttendanceLog.objects.create(
                        user=request.user,
                        log_type='check_in',
                        verification_method=verification_method,
                        ip_address=request.META.get('REMOTE_ADDR'),
                        device_info=request.META.get('HTTP_USER_AGENT', '')[:255]
                    )
                
                messages.success(request, f'Attendance updated successfully using {verification_method} verification!')
            
            return redirect('attendance:attendance_home')
    else:
        form = AttendanceForm(instance=attendance)
    
    context = {
        'form': form,
        'attendance': attendance,
        'created': created,
        'face_recognition_enabled': hasattr(request.user, 'profile') and request.user.profile.face_recognition_enabled
    }
    
    return render(request, 'attendance/mark_attendance.html', context)

@login_required
def attendance_history(request):
    """View attendance history"""
    # Default to current month
    today = timezone.now().date()
    start_date = datetime.date(today.year, today.month, 1)
    end_date = (datetime.date(today.year, today.month + 1, 1) 
                if today.month < 12 
                else datetime.date(today.year + 1, 1, 1)) - datetime.timedelta(days=1)
    
    # Get employees list for staff users
    employees = None
    if request.user.is_staff:
        employees = User.objects.filter(is_active=True).order_by('username')
    
    # Process GET parameters for filtering
    if request.method == 'GET':
        form = DateRangeForm(request.GET)
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date', start_date)
            end_date = form.cleaned_data.get('end_date', end_date)
            selected_user = form.cleaned_data.get('user')
        else:
            form = DateRangeForm(initial={'start_date': start_date, 'end_date': end_date})
            selected_user = None
    else:
        form = DateRangeForm(initial={'start_date': start_date, 'end_date': end_date})
        selected_user = None
    
    # Filter attendance records
    if request.user.is_staff and selected_user:
        attendance_list = Attendance.objects.filter(
            user=selected_user,
            date__gte=start_date,
            date__lte=end_date
        ).order_by('-date')
    elif request.user.is_staff and not selected_user:
        attendance_list = Attendance.objects.filter(
            date__gte=start_date,
            date__lte=end_date
        ).order_by('-date')
    else:
        attendance_list = Attendance.objects.filter(
            user=request.user,
            date__gte=start_date,
            date__lte=end_date
        ).order_by('-date')
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(attendance_list, 10)  # Show 10 records per page
    page = request.GET.get('page')
    try:
        attendance_records = paginator.page(page)
    except:
        # If page is not an integer or out of range, deliver first page
        attendance_records = paginator.page(1)
    
    context = {
        'form': form,
        'attendance_records': attendance_records,
        'start_date': start_date,
        'employees': employees,
        'end_date': end_date,
    }
    
    return render(request, 'attendance/history.html', context)

@login_required
def attendance_report(request):
    """Generate attendance report"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('users:dashboard')
    
    # Get employees list for staff users
    employees = User.objects.filter(is_active=True).order_by('username')
    
    # Default to current month
    today = timezone.now().date()
    start_date = datetime.date(today.year, today.month, 1)
    end_date = today
    
    preview = False
    attendance_records = []
    summary_data = []
    download_url = None
    
    if request.method == 'GET' and request.GET:
        form = DateRangeForm(request.GET)
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date', start_date)
            end_date = form.cleaned_data.get('end_date', end_date)
            selected_user = form.cleaned_data.get('user')
            report_type = request.GET.get('report_type', 'detailed')
            report_format = request.GET.get('format', 'csv')
            
            # Filter attendance records
            query = Q(date__gte=start_date) & Q(date__lte=end_date)
            if selected_user:
                query &= Q(user=selected_user)
            
            attendance_records = Attendance.objects.filter(query).order_by('user__username', 'date')
            
            # Generate preview if requested
            if 'preview' in request.GET:
                preview = True
                
                # Generate summary data if summary report type is selected
                if report_type == 'summary':
                    # This is a simplified example - in a real app, you'd calculate these metrics
                    summary_data = []
                    if selected_user:
                        users = [selected_user]
                    else:
                        users = User.objects.filter(attendance__in=attendance_records).distinct()
                    
                    for user in users:
                        user_records = attendance_records.filter(user=user)
                        present_days = user_records.filter(is_present=True).count()
                        total_days = user_records.count()
                        
                        total_hours = sum([r.get_duration_hours() for r in user_records if r.check_in_time and r.check_out_time], 0)
                        avg_hours = total_hours / present_days if present_days > 0 else 0
                        
                        summary_data.append({
                            'user': user,
                            'total_days': total_days,
                            'present_days': present_days,
                            'absent_days': total_days - present_days,
                            'late_arrivals': 0,  # Would calculate based on company policy
                            'early_departures': 0,  # Would calculate based on company policy
                            'total_hours': round(total_hours, 2),
                            'avg_hours_per_day': round(avg_hours, 2)
                        })
                
                # Create download URL for the actual report
                params = request.GET.copy()
                params.pop('preview', None)
                download_url = f"{request.path}?{params.urlencode()}"
            
            # Generate actual report file if not preview
            elif report_format == 'csv':
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="attendance_report_{start_date}_to_{end_date}.csv"'
                
                writer = csv.writer(response)
                
                if report_type == 'detailed':
                    writer.writerow(['Username', 'Employee ID', 'Date', 'Check-in Time', 'Check-out Time', 'Duration', 'Type', 'Status', 'Notes'])
                    
                    for record in attendance_records:
                        writer.writerow([
                            record.user.username,
                            getattr(record.user.profile, 'employee_id', 'N/A') if hasattr(record.user, 'profile') else 'N/A',
                            record.date,
                            record.check_in_time.strftime('%H:%M:%S') if record.check_in_time else 'N/A',
                            record.check_out_time.strftime('%H:%M:%S') if record.check_out_time else 'N/A',
                            record.get_duration(),
                            record.attendance_type,
                            'Present' if record.is_present else 'Absent',
                            record.notes or 'N/A'
                        ])
                else:  # summary report
                    writer.writerow(['Username', 'Employee ID', 'Total Days', 'Present Days', 'Absent Days', 'Total Hours', 'Avg Hours/Day'])
                    
                    # Generate summary data
                    if selected_user:
                        users = [selected_user]
                    else:
                        users = User.objects.filter(attendance__in=attendance_records).distinct()
                    
                    for user in users:
                        user_records = attendance_records.filter(user=user)
                        present_days = user_records.filter(is_present=True).count()
                        total_days = user_records.count()
                        
                        total_hours = sum([r.get_duration_hours() for r in user_records if r.check_in_time and r.check_out_time], 0)
                        avg_hours = total_hours / present_days if present_days > 0 else 0
                        
                        writer.writerow([
                            user.username,
                            getattr(user.profile, 'employee_id', 'N/A') if hasattr(user, 'profile') else 'N/A',
                            total_days,
                            present_days,
                            total_days - present_days,
                            round(total_hours, 2),
                            round(avg_hours, 2)
                        ])
                
                return response
            
            # Handle Excel and PDF formats (placeholder - would implement with appropriate libraries)
            elif report_format in ['excel', 'pdf']:
                messages.info(request, f'{report_format.upper()} export is not implemented in this demo.')
                return redirect('attendance:attendance_report')
    else:
        form = DateRangeForm(initial={'start_date': start_date, 'end_date': end_date})
    
    context = {
        'form': form,
        'attendance_records': attendance_records,
        'summary_data': summary_data,
        'preview': preview,
        'download_url': download_url,
        'employees': employees,
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'attendance/report.html', context)

@login_required
def upload_face(request):
    """Upload face image for recognition"""
    from .face_recognition_utils import process_uploaded_image, detect_faces, extract_face_features, save_face_encoding
    
    if request.method == 'POST':
        if 'face_image' in request.FILES:
            # Validate file type
            file = request.FILES['face_image']
            if not file.content_type.startswith('image/'):
                messages.error(request, 'Please upload a valid image file.')
                return render(request, 'attendance/upload_face.html')
            
            # Check file size (5MB limit)
            if file.size > 5 * 1024 * 1024:
                messages.error(request, 'File size must be less than 5MB.')
                return render(request, 'attendance/upload_face.html')
            
            # Process the uploaded image for face recognition
            image_array = process_uploaded_image(file)
            if image_array is None:
                messages.error(request, 'Could not process the uploaded image. Please try again with a different image.')
                return render(request, 'attendance/upload_face.html')
            
            # Detect faces in the image
            face_locations = detect_faces(image_array)
            
            if not face_locations:
                messages.error(request, 'No face detected in the uploaded image. Please upload a clear image of your face.')
                return render(request, 'attendance/upload_face.html')
            
            if len(face_locations) > 1:
                messages.error(request, 'Multiple faces detected in the image. Please upload an image with only your face.')
                return render(request, 'attendance/upload_face.html')
            
            # Extract face features
            face_features = extract_face_features(image_array, face_locations)
            
            if not face_features:
                messages.error(request, 'Could not extract facial features. Please upload a clearer image.')
                return render(request, 'attendance/upload_face.html')
            
            # Save the face image
            request.user.profile.face_image = file
            
            # Save the face features
            if save_face_encoding(request.user, face_features[0]):
                # Enable face recognition for this user
                request.user.profile.face_recognition_enabled = True
                request.user.profile.save()
                messages.success(request, 'Face image uploaded and processed successfully! Face recognition is now enabled for your account.')
            else:
                request.user.profile.save()
                messages.warning(request, 'Face image uploaded but there was an issue processing the facial features. Face recognition may not work properly.')
            
            return redirect('users:profile')
        else:
            messages.error(request, 'No image file provided.')
    
    return render(request, 'attendance/upload_face.html')

@login_required
def upload_fingerprint(request):
    """Upload fingerprint data"""
    if request.method == 'POST':
        if 'fingerprint_data' in request.FILES:
            request.user.profile.fingerprint_data = request.FILES['fingerprint_data']
            request.user.profile.save()
            messages.success(request, 'Fingerprint data uploaded successfully!')
            return redirect('users:profile')
        else:
            messages.error(request, 'No fingerprint data provided.')
    
    return render(request, 'attendance/upload_fingerprint.html')

@login_required
def test_camera(request):
    """Test camera functionality"""
    return render(request, 'attendance/test_camera.html')

@login_required
def debug_camera(request):
    """Debug camera functionality"""
    return render(request, 'attendance/debug_camera.html')
