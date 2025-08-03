// Main JavaScript file for Attendance Management System

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Current time display for attendance pages
    updateCurrentTime();
    setInterval(updateCurrentTime, 1000);

    // Initialize face recognition if on the appropriate page
    if (document.getElementById('face-capture-container')) {
        initFaceCapture();
    }

    // Initialize fingerprint scanner if on the appropriate page
    if (document.getElementById('fingerprint-scanner-container')) {
        initFingerprintScanner();
    }

    // Form validation for all forms
    validateForms();
});

// Update current time display
function updateCurrentTime() {
    const currentTimeElement = document.getElementById('current-time');
    if (currentTimeElement) {
        const now = new Date();
        const hours = now.getHours().toString().padStart(2, '0');
        const minutes = now.getMinutes().toString().padStart(2, '0');
        const seconds = now.getSeconds().toString().padStart(2, '0');
        currentTimeElement.textContent = `${hours}:${minutes}:${seconds}`;
    }
}

// Initialize face capture functionality
function initFaceCapture() {
    const videoElement = document.getElementById('video');
    const canvasElement = document.getElementById('canvas');
    const captureButton = document.getElementById('capture-button');
    const retakeButton = document.getElementById('retake-button');
    const resultContainer = document.getElementById('result-container');
    const faceImageInput = document.getElementById('face_image');

    // Variables to store stream and capture status
    let stream = null;
    let captureComplete = false;

    // Function to start the camera
    async function startCamera() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: true });
            videoElement.srcObject = stream;
            videoElement.style.display = 'block';
            canvasElement.style.display = 'none';
            captureButton.style.display = 'block';
            retakeButton.style.display = 'none';
            resultContainer.style.display = 'none';
            captureComplete = false;
        } catch (err) {
            console.error('Error accessing camera:', err);
            alert('Error accessing camera. Please make sure your camera is connected and you have given permission to use it.');
        }
    }

    // Function to capture image from video
    function captureImage() {
        if (!stream) return;

        const context = canvasElement.getContext('2d');
        canvasElement.width = videoElement.videoWidth;
        canvasElement.height = videoElement.videoHeight;
        context.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
        
        // Convert canvas to blob for form submission
        canvasElement.toBlob(function(blob) {
            const file = new File([blob], 'face_capture.png', { type: 'image/png' });
            
            // Create a FileList-like object
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            faceImageInput.files = dataTransfer.files;
            
            // Display the captured image
            videoElement.style.display = 'none';
            canvasElement.style.display = 'block';
            captureButton.style.display = 'none';
            retakeButton.style.display = 'block';
            resultContainer.style.display = 'block';
            resultContainer.innerHTML = '<div class="alert alert-success">Image captured successfully!</div>';
            captureComplete = true;
            
            // Stop the camera stream
            stopCamera();
        }, 'image/png');
    }

    // Function to stop the camera stream
    function stopCamera() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            stream = null;
        }
    }

    // Event listeners
    if (captureButton) {
        captureButton.addEventListener('click', captureImage);
    }

    if (retakeButton) {
        retakeButton.addEventListener('click', startCamera);
    }

    // Start camera when page loads
    if (videoElement && canvasElement) {
        startCamera();
    }

    // Clean up when leaving the page
    window.addEventListener('beforeunload', stopCamera);
}

// Initialize fingerprint scanner functionality
function initFingerprintScanner() {
    const scanButton = document.getElementById('scan-button');
    const rescanButton = document.getElementById('rescan-button');
    const scannerContainer = document.getElementById('scanner-container');
    const resultContainer = document.getElementById('fingerprint-result');
    const fingerprintInput = document.getElementById('fingerprint_data');

    // Simulate fingerprint scanning
    function simulateScan() {
        scannerContainer.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Scanning...</span></div><p class="mt-2">Scanning fingerprint...</p></div>';
        
        // Simulate scanning delay
        setTimeout(function() {
            // Create a mock fingerprint data file
            const mockData = new Blob(['MOCK_FINGERPRINT_DATA_' + Date.now()], { type: 'application/octet-stream' });
            const file = new File([mockData], 'fingerprint.dat', { type: 'application/octet-stream' });
            
            // Create a FileList-like object
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            fingerprintInput.files = dataTransfer.files;
            
            // Update UI
            scannerContainer.innerHTML = '<div class="text-center"><i class="fas fa-fingerprint fa-5x text-success"></i><p class="mt-2">Scan complete!</p></div>';
            resultContainer.innerHTML = '<div class="alert alert-success">Fingerprint scanned successfully!</div>';
            scanButton.style.display = 'none';
            rescanButton.style.display = 'block';
        }, 2000);
    }

    // Event listeners
    if (scanButton) {
        scanButton.addEventListener('click', simulateScan);
    }

    if (rescanButton) {
        rescanButton.addEventListener('click', function() {
            scannerContainer.innerHTML = '<div class="text-center"><i class="fas fa-fingerprint fa-5x text-primary"></i><p class="mt-2">Ready to scan</p></div>';
            resultContainer.innerHTML = '';
            scanButton.style.display = 'block';
            rescanButton.style.display = 'none';
        });
    }
}

// Form validation for all forms
function validateForms() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
}

// Function to handle attendance marking
function markAttendance(type) {
    const attendanceTypeInput = document.getElementById('attendance_type');
    if (attendanceTypeInput) {
        attendanceTypeInput.value = type;
    }
    
    // Submit the form
    const attendanceForm = document.getElementById('attendance-form');
    if (attendanceForm) {
        attendanceForm.submit();
    }
}

// Function to toggle verification method in attendance marking
function toggleVerificationMethod(method) {
    const manualSection = document.getElementById('manual-verification');
    const faceSection = document.getElementById('face-verification');
    const fingerprintSection = document.getElementById('fingerprint-verification');
    const verificationMethodInput = document.getElementById('verification_method');
    
    // Hide all sections first
    if (manualSection) manualSection.style.display = 'none';
    if (faceSection) faceSection.style.display = 'none';
    if (fingerprintSection) fingerprintSection.style.display = 'none';
    
    // Show the selected section
    if (method === 'manual' && manualSection) {
        manualSection.style.display = 'block';
    } else if (method === 'face' && faceSection) {
        faceSection.style.display = 'block';
        // Initialize face capture if needed
        if (typeof initFaceCapture === 'function') {
            initFaceCapture();
        }
    } else if (method === 'fingerprint' && fingerprintSection) {
        fingerprintSection.style.display = 'block';
        // Initialize fingerprint scanner if needed
        if (typeof initFingerprintScanner === 'function') {
            initFingerprintScanner();
        }
    }
    
    // Update the hidden input
    if (verificationMethodInput) {
        verificationMethodInput.value = method;
    }
}

// Function to handle date range selection in reports
function updateDateRange(preset) {
    const startDateInput = document.getElementById('start_date');
    const endDateInput = document.getElementById('end_date');
    
    if (!startDateInput || !endDateInput) return;
    
    const today = new Date();
    let startDate = new Date();
    
    switch(preset) {
        case 'today':
            // Start and end are both today
            break;
        case 'yesterday':
            startDate.setDate(today.getDate() - 1);
            endDateInput.valueAsDate = startDate;
            break;
        case 'thisWeek':
            // Start date is the first day of current week (Sunday)
            startDate.setDate(today.getDate() - today.getDay());
            break;
        case 'lastWeek':
            // Start date is the first day of last week
            startDate.setDate(today.getDate() - today.getDay() - 7);
            // End date is the last day of last week
            const endLastWeek = new Date(startDate);
            endLastWeek.setDate(startDate.getDate() + 6);
            endDateInput.valueAsDate = endLastWeek;
            break;
        case 'thisMonth':
            // Start date is the first day of current month
            startDate.setDate(1);
            break;
        case 'lastMonth':
            // Start date is the first day of last month
            startDate.setMonth(today.getMonth() - 1);
            startDate.setDate(1);
            // End date is the last day of last month
            const endLastMonth = new Date(today.getFullYear(), today.getMonth(), 0);
            endDateInput.valueAsDate = endLastMonth;
            break;
        default:
            return;
    }
    
    startDateInput.valueAsDate = startDate;
    if (preset === 'today' || preset === 'thisWeek' || preset === 'thisMonth') {
        endDateInput.valueAsDate = today;
    }
}

// Function to preview report before generating
function previewReport() {
    const startDate = document.getElementById('start_date').value;
    const endDate = document.getElementById('end_date').value;
    const employee = document.getElementById('employee') ? document.getElementById('employee').value : 'all';
    const reportType = document.querySelector('input[name="report_type"]:checked').value;
    
    const previewContainer = document.getElementById('report-preview');
    if (!previewContainer) return;
    
    // Show loading indicator
    previewContainer.innerHTML = '<div class="text-center p-4"><div class="spinner-border text-primary" role="status"></div><p class="mt-2">Generating preview...</p></div>';
    
    // In a real application, this would make an AJAX request to get the preview data
    // For this demo, we'll simulate it with a timeout
    setTimeout(function() {
        let previewHTML = `
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Report Preview</h5>
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        <strong>Date Range:</strong> ${startDate} to ${endDate}<br>
                        <strong>Employee:</strong> ${employee === 'all' ? 'All Employees' : 'Selected Employee'}<br>
                        <strong>Report Type:</strong> ${reportType === 'detailed' ? 'Detailed Report' : 'Summary Report'}
                    </div>
        `;
        
        if (reportType === 'detailed') {
            previewHTML += `
                <div class="table-responsive">
                    <table class="table table-bordered table-hover">
                        <thead class="table-light">
                            <tr>
                                <th>Date</th>
                                <th>Employee</th>
                                <th>Check In</th>
                                <th>Check Out</th>
                                <th>Duration</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Sample data</td>
                                <td>Sample data</td>
                                <td>Sample data</td>
                                <td>Sample data</td>
                                <td>Sample data</td>
                                <td><span class="badge bg-success">Present</span></td>
                            </tr>
                            <tr>
                                <td>Sample data</td>
                                <td>Sample data</td>
                                <td>Sample data</td>
                                <td>Sample data</td>
                                <td>Sample data</td>
                                <td><span class="badge bg-warning">Late</span></td>
                            </tr>
                            <tr>
                                <td>Sample data</td>
                                <td>Sample data</td>
                                <td>Sample data</td>
                                <td>Sample data</td>
                                <td>Sample data</td>
                                <td><span class="badge bg-danger">Absent</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            `;
        } else {
            previewHTML += `
                <div class="table-responsive">
                    <table class="table table-bordered table-hover">
                        <thead class="table-light">
                            <tr>
                                <th>Employee</th>
                                <th>Present Days</th>
                                <th>Absent Days</th>
                                <th>Late Days</th>
                                <th>Total Hours</th>
                                <th>Attendance %</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Sample data</td>
                                <td>Sample data</td>
                                <td>Sample data</td>
                                <td>Sample data</td>
                                <td>Sample data</td>
                                <td>Sample data</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            `;
        }
        
        previewHTML += `
                </div>
                <div class="card-footer">
                    <small class="text-muted">This is a preview. The actual report may contain more data.</small>
                </div>
            </div>
        `;
        
        previewContainer.innerHTML = previewHTML;
    }, 1000);
}