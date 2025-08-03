# Attendance Management System

## Overview
A comprehensive Django-based attendance management system with face recognition and fingerprint verification capabilities. This system allows organizations to track employee attendance efficiently with multiple verification methods.

## Features
- **Multiple Authentication Methods**:
  - **Face Recognition** (✅ Implemented with real camera access)
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
- **Camera Integration**:
  - Real-time camera access using Web API
  - Face detection and capture
  - Image processing and validation
  - Secure file upload handling

## Technology Stack
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: SQLite (default), compatible with PostgreSQL, MySQL
- **Authentication**: Django Authentication System
- **Camera Integration**: Web MediaDevices API, Canvas API for image processing
- **Biometric Integration**: JavaScript APIs for camera and fingerprint scanner

## Installation

### Quick Start (Recommended)
```bash
# Clone the repository
git clone https://github.com/Abhishek-max825/project_django.git
cd project_django

# Run the automated installation script
python install.py
```

### Manual Installation

#### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

#### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Abhishek-max825/project_django.git
   cd project_django
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/
   - Camera test: http://127.0.0.1:8000/attendance/test-camera/

### Platform-Specific Notes

#### Windows
- No additional system dependencies required
- OpenCV will be installed automatically via pip

#### Linux
- May need to install OpenCV system dependencies:
  ```bash
  sudo apt install libgl1-mesa-glx libglib2.0-0
  ```

#### macOS
- Install OpenCV via Homebrew:
  ```bash
  brew install opencv
  ```

### Troubleshooting Installation

If you encounter issues:

1. **Check Python version**: Ensure you have Python 3.8+
2. **Use the installation script**: `python install.py`
3. **Check platform-specific requirements** in DEPLOYMENT_GUIDE.md
4. **Verify virtual environment**: Make sure it's activated
5. **Check pip**: Ensure pip is up to date

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

### Camera Functionality
1. **Face Upload**: Navigate to "Upload Face" to capture your face image using your device's camera
2. **Attendance Marking**: When marking attendance, select "Face Recognition" as verification method
3. **Camera Access**: The system will request camera permissions - allow access for face verification
4. **Face Detection**: The system includes basic face detection to ensure a face is visible in the captured image
5. **Image Processing**: Captured images are processed and stored securely for attendance verification

#### Camera Requirements
- Modern web browser with camera support (Chrome, Firefox, Safari, Edge)
- HTTPS connection (required for camera access in most browsers)
- Camera permissions granted to the website
- Front-facing camera recommended for best results

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