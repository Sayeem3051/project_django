#!/usr/bin/env python
import os
import sys
import django
import sqlite3

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import Profile
from attendance.models import Attendance, AttendanceLog

def check_database():
    print("=== DATABASE CONTENTS ===")
    print()
    
    # Check Users
    print("=== USERS ===")
    users = User.objects.all()
    print(f"Total users: {users.count()}")
    for user in users:
        print(f"  - {user.username} ({user.email}) - Created: {user.date_joined}")
    print()
    
    # Check Profiles
    print("=== PROFILES ===")
    profiles = Profile.objects.all()
    print(f"Total profiles: {profiles.count()}")
    for profile in profiles:
        print(f"  - User: {profile.user.username}")
        print(f"    Employee ID: {profile.employee_id}")
        print(f"    Department: {profile.department}")
        print(f"    Position: {profile.position}")
        print(f"    Phone: {profile.phone_number}")
        print(f"    Face Image: {profile.face_image}")
        print(f"    Face Encoding: {profile.face_encoding_path}")
        print(f"    Face Recognition Enabled: {profile.face_recognition_enabled}")
        print(f"    Fingerprint Data: {profile.fingerprint_data}")
        print(f"    Date Joined: {profile.date_joined}")
        print()
    
    # Check Attendance
    print("=== ATTENDANCE RECORDS ===")
    attendance_records = Attendance.objects.all()
    print(f"Total attendance records: {attendance_records.count()}")
    for record in attendance_records:
        print(f"  - User: {record.user.username}")
        print(f"    Date: {record.date}")
        print(f"    Check In: {record.check_in_time}")
        print(f"    Check Out: {record.check_out_time}")
        print(f"    Attendance Type: {record.attendance_type}")
        print(f"    Is Present: {record.is_present}")
        print(f"    Notes: {record.notes}")
        print(f"    Duration: {record.get_duration()}")
        print()
    
    # Check Attendance Logs
    print("=== ATTENDANCE LOGS ===")
    attendance_logs = AttendanceLog.objects.all()
    print(f"Total attendance logs: {attendance_logs.count()}")
    for log in attendance_logs:
        print(f"  - User: {log.user.username}")
        print(f"    Timestamp: {log.timestamp}")
        print(f"    Log Type: {log.log_type}")
        print(f"    Verification Method: {log.verification_method}")
        print(f"    Success: {log.success}")
        print(f"    IP Address: {log.ip_address}")
        print(f"    Device Info: {log.device_info}")
        print()
    
    # Check database tables directly
    print("=== DATABASE TABLES ===")
    db_path = 'db.sqlite3'
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"Total tables: {len(tables)}")
        for table in tables:
            table_name = table[0]
            print(f"\n--- Table: {table_name} ---")
            
            # Get table info
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            print("Columns:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"Rows: {count}")
            
            # Show first few rows
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
                rows = cursor.fetchall()
                print("Sample data:")
                for row in rows:
                    print(f"  {row}")
        
        conn.close()
    else:
        print("Database file not found!")

if __name__ == "__main__":
    check_database() 