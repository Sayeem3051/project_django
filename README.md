# Attendance Management System

## Overview
A comprehensive Django-based attendance management system with face recognition and fingerprint verification capabilities. This system allows organizations to track employee attendance efficiently with multiple verification methods.

## Features
- **Multiple Authentication Methods**:
  - Face Recognition
  - Fingerprint Scanning
  - Manual Entry
- **User Management**:
  - User Registration
  - Profile Management
  - Role-based Access Control
- **Attendance Tracking**:
  - Check-in/Check-out Recording
  - Attendance History
  - Attendance Reports
- **Reporting**:
  - Detailed and Summary Reports
  - Export to CSV
  - Date Range Filtering
- **Admin Dashboard**:
  - User Management
  - Attendance Overview
  - System Configuration

## Technology Stack
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: SQLite (default), compatible with PostgreSQL, MySQL
- **Authentication**: Django Authentication System
- **Biometric Integration**: JavaScript APIs for camera and fingerprint scanner

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**
   ```
   git clone <repository-url>
   cd project_new
   ```

2. **Create and activate a virtual environment**
   ```
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```
   python manage.py migrate
   ```

5. **Create a superuser**
   ```
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```
   python manage.py runserver
   ```

7. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/

## Usage

### Admin User
1. Log in to the admin interface using the superuser credentials
2. Manage users, departments, and attendance records
3. Generate and export attendance reports

### Regular User
1. Register a new account or log in with existing credentials
2. Set up your profile with required information
3. Upload face image and/or fingerprint data for biometric verification
4. Mark attendance using preferred verification method
5. View attendance history and personal reports

## Project Structure

```
attendance_system/
├── attendance/            # Attendance app
│   ├── admin.py           # Admin configuration
│   ├── forms.py           # Form definitions
│   ├── models.py          # Data models
│   ├── urls.py            # URL routing
│   └── views.py           # View functions
├── users/                 # Users app
│   ├── admin.py           # Admin configuration
│   ├── forms.py           # Form definitions
│   ├── models.py          # Data models
│   ├── urls.py            # URL routing
│   └── views.py           # View functions
├── attendance_system/     # Project settings
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # WSGI configuration
├── static/                # Static files
│   ├── css/               # CSS files
│   ├── js/                # JavaScript files
│   └── img/               # Image files
├── templates/             # HTML templates
│   ├── attendance/        # Attendance templates
│   └── users/             # User templates
├── media/                 # User-uploaded files
├── manage.py              # Django management script
└── requirements.txt       # Project dependencies
```

## Security Considerations
- Biometric data is stored securely and used only for attendance verification
- User passwords are hashed and not stored in plaintext
- CSRF protection is enabled for all forms
- User permissions are strictly enforced

## Future Enhancements
- Mobile application integration
- Real-time notifications
- Advanced analytics dashboard
- Integration with HR systems
- Geolocation-based attendance

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contributors
- [Your Name] - Initial work