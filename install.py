#!/usr/bin/env python3
"""
Installation Script for Attendance Management System
This script automates the setup process for different platforms.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_system_dependencies():
    """Install system dependencies based on platform"""
    system = platform.system().lower()
    
    if system == "linux":
        print("🐧 Installing Linux dependencies...")
        commands = [
            "sudo apt update",
            "sudo apt install -y python3-pip python3-venv libgl1-mesa-glx libglib2.0-0"
        ]
    elif system == "darwin":  # macOS
        print("🍎 Installing macOS dependencies...")
        commands = [
            "brew install opencv",
            "brew install python3"
        ]
    elif system == "windows":
        print("🪟 Windows detected - no additional system dependencies needed")
        return True
    else:
        print(f"⚠️  Unknown system: {system}")
        return True
    
    for command in commands:
        if not run_command(command, f"Running: {command}"):
            print(f"⚠️  Warning: {command} failed, but continuing...")
    
    return True

def create_virtual_environment():
    """Create and activate virtual environment"""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("📁 Virtual environment already exists")
        return True
    
    print("📁 Creating virtual environment...")
    if not run_command("python -m venv venv", "Creating virtual environment"):
        return False
    
    return True

def install_python_dependencies():
    """Install Python dependencies"""
    # Determine activation command based on platform
    if platform.system().lower() == "windows":
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    # Install dependencies
    if not run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip"):
        return False
    
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing Python dependencies"):
        return False
    
    return True

def setup_django():
    """Setup Django project"""
    # Determine python command based on platform
    if platform.system().lower() == "windows":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"
    
    commands = [
        (f"{python_cmd} manage.py makemigrations", "Creating database migrations"),
        (f"{python_cmd} manage.py migrate", "Running database migrations"),
        (f"{python_cmd} manage.py collectstatic --noinput", "Collecting static files")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True

def create_superuser():
    """Create a superuser account"""
    print("👤 Creating superuser account...")
    print("Please enter the following information:")
    
    # Determine python command based on platform
    if platform.system().lower() == "windows":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"
    
    command = f"{python_cmd} manage.py createsuperuser"
    
    try:
        subprocess.run(command, shell=True, check=True)
        print("✅ Superuser created successfully")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  Superuser creation failed or was cancelled")
        return True  # Don't fail the installation for this

def print_success_message():
    """Print success message with next steps"""
    print("\n" + "="*60)
    print("🎉 INSTALLATION COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\n📋 Next Steps:")
    print("1. Start the server:")
    if platform.system().lower() == "windows":
        print("   venv\\Scripts\\activate")
        print("   python manage.py runserver")
    else:
        print("   source venv/bin/activate")
        print("   python manage.py runserver")
    
    print("\n2. Access the application:")
    print("   - Main app: http://127.0.0.1:8000/")
    print("   - Admin panel: http://127.0.0.1:8000/admin/")
    print("   - Camera test: http://127.0.0.1:8000/attendance/test-camera/")
    
    print("\n3. Test the system:")
    print("   - Upload a face image for recognition")
    print("   - Test camera functionality")
    print("   - Mark attendance with face recognition")
    
    print("\n📚 Documentation:")
    print("   - See DEPLOYMENT_GUIDE.md for detailed instructions")
    print("   - Check README.md for feature overview")
    
    print("\n🔧 Troubleshooting:")
    print("   - If camera doesn't work, ensure HTTPS is enabled")
    print("   - Check browser permissions for camera access")
    print("   - Use the test camera page to debug issues")
    
    print("\n🚀 Ready to use your Attendance Management System!")

def main():
    """Main installation function"""
    print("🚀 Attendance Management System - Installation Script")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install system dependencies
    if not install_system_dependencies():
        print("⚠️  System dependency installation had issues, but continuing...")
    
    # Create virtual environment
    if not create_virtual_environment():
        print("❌ Failed to create virtual environment")
        sys.exit(1)
    
    # Install Python dependencies
    if not install_python_dependencies():
        print("❌ Failed to install Python dependencies")
        sys.exit(1)
    
    # Setup Django
    if not setup_django():
        print("❌ Failed to setup Django")
        sys.exit(1)
    
    # Create superuser
    create_superuser()
    
    # Print success message
    print_success_message()

if __name__ == "__main__":
    main() 