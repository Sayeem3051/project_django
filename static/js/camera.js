// Camera functionality for Attendance Management System

class CameraManager {
    constructor() {
        this.stream = null;
        this.video = null;
        this.canvas = null;
        this.isCapturing = false;
        this.faceDetectionModel = null;
        this.isModelLoaded = false;
    }

    // Initialize camera functionality
    async initCamera(containerId, videoId, canvasId) {
        console.log('CameraManager: Initializing camera...');
        
        // Check if MediaDevices API is available
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            console.error('MediaDevices API not supported');
            this.showError('Camera access not supported in this browser. Please use a modern browser.');
            return false;
        }

        this.video = document.getElementById(videoId);
        this.canvas = document.getElementById(canvasId);
        
        if (!this.video || !this.canvas) {
            console.error('Video or canvas element not found');
            this.showError('Camera elements not found. Please refresh the page.');
            return false;
        }

        try {
            console.log('Requesting camera access...');
            // Request camera access with specific constraints
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: 'user' // Use front camera
                }
            });

            console.log('Camera access granted, setting up video...');
            this.video.srcObject = this.stream;
            
            // Wait for video to be ready
            await new Promise((resolve, reject) => {
                this.video.addEventListener('loadedmetadata', resolve);
                this.video.addEventListener('error', reject);
                this.video.play().catch(reject);
            });

            // Set up canvas dimensions
            this.canvas.width = this.video.videoWidth;
            this.canvas.height = this.video.videoHeight;
            
            console.log('Camera initialized successfully');
            return true;
        } catch (error) {
            console.error('Error accessing camera:', error);
            let errorMessage = 'Camera access denied. ';
            
            if (error.name === 'NotAllowedError') {
                errorMessage += 'Please allow camera permissions and refresh the page.';
            } else if (error.name === 'NotFoundError') {
                errorMessage += 'No camera found. Please connect a camera and try again.';
            } else if (error.name === 'NotSupportedError') {
                errorMessage += 'Camera not supported. Please use a different browser.';
            } else {
                errorMessage += error.message;
            }
            
            this.showError(errorMessage);
            return false;
        }
    }

    // Stop camera stream
    stopCamera() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
        if (this.video) {
            this.video.srcObject = null;
        }
    }

    // Capture image from video stream
    captureImage() {
        if (!this.video || !this.canvas) {
            console.error('Video or canvas not available');
            return null;
        }

        const context = this.canvas.getContext('2d');
        context.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
        
        return this.canvas.toDataURL('image/jpeg', 0.8);
    }

    // Convert data URL to blob
    dataURLToBlob(dataURL) {
        const arr = dataURL.split(',');
        const mime = arr[0].match(/:(.*?);/)[1];
        const bstr = atob(arr[1]);
        let n = bstr.length;
        const u8arr = new Uint8Array(n);
        
        while (n--) {
            u8arr[n] = bstr.charCodeAt(n);
        }
        
        return new Blob([u8arr], { type: mime });
    }

    // Face detection using basic image analysis
    async detectFace(imageData) {
        return new Promise((resolve) => {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            const img = new Image();
            
            img.onload = () => {
                canvas.width = img.width;
                canvas.height = img.height;
                ctx.drawImage(img, 0, 0);
                
                const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                const data = imageData.data;
                
                // Enhanced face detection using multiple criteria
                let skinPixels = 0;
                let totalPixels = data.length / 4;
                let edgePixels = 0;
                
                for (let i = 0; i < data.length; i += 4) {
                    const r = data[i];
                    const g = data[i + 1];
                    const b = data[i + 2];
                    
                    // Enhanced skin tone detection
                    if (r > 95 && g > 40 && b > 20 && 
                        Math.max(r, g, b) - Math.min(r, g, b) > 15 &&
                        Math.abs(r - g) > 15 && r > g && r > b) {
                        skinPixels++;
                    }
                    
                    // Edge detection for facial features
                    if (i > 0 && i < data.length - 4) {
                        const currentBrightness = (r + g + b) / 3;
                        const nextBrightness = (data[i + 4] + data[i + 5] + data[i + 6]) / 3;
                        if (Math.abs(currentBrightness - nextBrightness) > 30) {
                            edgePixels++;
                        }
                    }
                }
                
                const skinPercentage = (skinPixels / totalPixels) * 100;
                const edgePercentage = (edgePixels / totalPixels) * 100;
                
                // More sophisticated face detection criteria
                const hasFace = skinPercentage > 8 && edgePercentage > 2 && edgePercentage < 15;
                
                resolve({
                    hasFace: hasFace,
                    confidence: Math.min(skinPercentage / 100, 0.9),
                    message: hasFace ? 'Face detected successfully' : 'No face detected in the image'
                });
            };
            
            img.src = imageData;
        });
    }

    // Show error message
    showError(message) {
        const container = document.getElementById('camera-container');
        if (container) {
            container.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    ${message}
                </div>
            `;
        }
    }

    // Show success message
    showSuccess(message) {
        const container = document.getElementById('camera-container');
        if (container) {
            container.innerHTML = `
                <div class="alert alert-success">
                    <i class="fas fa-check-circle me-2"></i>
                    ${message}
                </div>
            `;
        }
    }

    // Show loading message
    showLoading(message = 'Processing...') {
        const container = document.getElementById('camera-container');
        if (container) {
            container.innerHTML = `
                <div class="text-center">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p class="mt-2">${message}</p>
                </div>
            `;
        }
    }
}

// Global camera manager instance
let cameraManager = null;

// Initialize camera functionality for attendance marking
function initAttendanceCamera() {
    console.log('Initializing attendance camera...');
    cameraManager = new CameraManager();
    
    const startCameraBtn = document.getElementById('start-camera');
    const captureBtn = document.getElementById('capture-face');
    const retakeBtn = document.getElementById('retake-face');
    const cameraContainer = document.getElementById('camera-container');
    
    if (!cameraContainer) {
        console.log('Camera container not found');
        return;
    }

    // Start camera button
    if (startCameraBtn) {
        startCameraBtn.addEventListener('click', async () => {
            console.log('Start camera button clicked');
            cameraContainer.innerHTML = `
                <div class="text-center">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Starting camera...</span>
                    </div>
                    <p class="mt-2">Starting camera...</p>
                </div>
            `;
            
            try {
                const success = await cameraManager.initCamera('camera-container', 'video', 'canvas');
                
                if (success) {
                    cameraContainer.innerHTML = `
                        <div class="position-relative">
                            <video id="video" autoplay muted playsinline style="width: 100%; max-width: 400px; height: auto;"></video>
                            <canvas id="canvas" style="display: none;"></canvas>
                            <div class="mt-3">
                                <button type="button" id="capture-face" class="btn btn-primary">
                                    <i class="fas fa-camera me-1"></i>Capture Face
                                </button>
                            </div>
                        </div>
                    `;
                    
                    // Re-attach event listeners
                    const newCaptureBtn = document.getElementById('capture-face');
                    if (newCaptureBtn) {
                        newCaptureBtn.addEventListener('click', handleFaceCapture);
                    }
                } else {
                    cameraContainer.innerHTML = `
                        <div class="alert alert-danger">
                            <i class="fas fa-exclamation-triangle me-2"></i>
                            Failed to start camera. Please check your camera permissions.
                        </div>
                    `;
                }
            } catch (error) {
                console.error('Camera initialization error:', error);
                cameraContainer.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="fas fa-exclamation-triangle me-2"></i>
                        Camera error: ${error.message}
                    </div>
                `;
            }
        });
    }

    // Handle face capture
    async function handleFaceCapture() {
        if (!cameraManager) return;
        
        cameraManager.showLoading('Capturing and analyzing face...');
        
        try {
            const imageData = cameraManager.captureImage();
            const faceResult = await cameraManager.detectFace(imageData);
            
            if (faceResult.hasFace) {
                // Convert image to blob and set form input
                const blob = cameraManager.dataURLToBlob(imageData);
                const file = new File([blob], 'face_capture.jpg', { type: 'image/jpeg' });
                
                // Create a FileList-like object
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                
                // Set the file input
                const faceImageInput = document.getElementById('face_image');
                
                // Update verification result
                const verificationResult = document.getElementById('face-verification-result');
                if (verificationResult) {
                    verificationResult.innerHTML = '<div class="alert alert-info"><i class="fas fa-spinner fa-spin me-2"></i>Face detected! Ready for server-side verification.</div>';
                }
                if (faceImageInput) {
                    faceImageInput.files = dataTransfer.files;
                }
                
                // Show captured image
                cameraContainer.innerHTML = `
                    <div class="text-center">
                        <img src="${imageData}" alt="Captured face" style="max-width: 400px; height: auto; border: 2px solid #28a745;">
                        <div class="mt-3">
                            <button type="button" id="retake-face" class="btn btn-outline-secondary">
                                <i class="fas fa-redo me-1"></i>Retake
                            </button>
                        </div>
                    </div>
                `;
                
                // Re-attach retake button
                const newRetakeBtn = document.getElementById('retake-face');
                if (newRetakeBtn) {
                    newRetakeBtn.addEventListener('click', () => {
                        initAttendanceCamera();
                    });
                }
                
                // Enable form submission
                const submitBtn = document.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = '<i class="fas fa-check-circle me-1"></i>Submit for Face Verification';
                }
                
            } else {
                cameraManager.showError('No face detected. Please ensure your face is clearly visible in the camera.');
                
                // Retry button
                setTimeout(() => {
                    cameraContainer.innerHTML += `
                        <div class="mt-3">
                            <button type="button" class="btn btn-outline-primary" onclick="initAttendanceCamera()">
                                <i class="fas fa-redo me-1"></i>Try Again
                            </button>
                        </div>
                    `;
                }, 2000);
            }
        } catch (error) {
            console.error('Error capturing face:', error);
            cameraManager.showError('Error capturing face. Please try again.');
        }
    }

    // Handle retake button
    if (retakeBtn) {
        retakeBtn.addEventListener('click', () => {
            initAttendanceCamera();
        });
    }
}

// Initialize camera for face upload page
function initFaceUploadCamera() {
    cameraManager = new CameraManager();
    
    const startCameraBtn = document.getElementById('start-camera');
    const captureBtn = document.getElementById('capture-button');
    const retakeBtn = document.getElementById('retake-button');
    const videoElement = document.getElementById('video');
    const canvasElement = document.getElementById('canvas');
    const faceImageInput = document.getElementById('face_image');
    
    if (!videoElement || !canvasElement) return;

    // Start camera
    async function startCamera() {
        try {
            const success = await cameraManager.initCamera('face-capture-container', 'video', 'canvas');
            
            if (success) {
                videoElement.style.display = 'block';
                canvasElement.style.display = 'none';
                if (captureBtn) captureBtn.style.display = 'block';
                if (retakeBtn) retakeBtn.style.display = 'none';
            }
        } catch (error) {
            console.error('Error starting camera:', error);
        }
    }

    // Capture image
    async function captureImage() {
        if (!cameraManager) return;
        
        try {
            const imageData = cameraManager.captureImage();
            const faceResult = await cameraManager.detectFace(imageData);
            
            if (faceResult.hasFace) {
                // Convert to blob and set form input
                const blob = cameraManager.dataURLToBlob(imageData);
                const file = new File([blob], 'face_upload.jpg', { type: 'image/jpeg' });
                
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                faceImageInput.files = dataTransfer.files;
                
                // Show captured image
                videoElement.style.display = 'none';
                canvasElement.style.display = 'block';
                if (captureBtn) captureBtn.style.display = 'none';
                if (retakeBtn) retakeBtn.style.display = 'block';
                
                // Update canvas with captured image
                const img = new Image();
                img.onload = () => {
                    const ctx = canvasElement.getContext('2d');
                    canvasElement.width = img.width;
                    canvasElement.height = img.height;
                    ctx.drawImage(img, 0, 0);
                };
                img.src = imageData;
                
                // Show success message
                const resultContainer = document.getElementById('result-container');
                if (resultContainer) {
                    resultContainer.innerHTML = '<div class="alert alert-success">Face image captured successfully!</div>';
                }
            } else {
                alert('No face detected. Please ensure your face is clearly visible and try again.');
            }
        } catch (error) {
            console.error('Error capturing image:', error);
            alert('Error capturing image. Please try again.');
        }
    }

    // Event listeners
    if (startCameraBtn) {
        startCameraBtn.addEventListener('click', startCamera);
    }
    
    if (captureBtn) {
        captureBtn.addEventListener('click', captureImage);
    }
    
    if (retakeBtn) {
        retakeBtn.addEventListener('click', startCamera);
    }

    // Start camera automatically
    startCamera();
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Camera.js: DOM loaded, initializing camera functionality...');
    
    // Check if we're on a page that needs camera functionality
    const cameraContainer = document.getElementById('camera-container');
    const faceCaptureContainer = document.getElementById('face-capture-container');
    
    console.log('Camera containers found:', {
        cameraContainer: !!cameraContainer,
        faceCaptureContainer: !!faceCaptureContainer
    });
    
    // Initialize camera for attendance marking page
    if (cameraContainer) {
        console.log('Initializing attendance camera...');
        initAttendanceCamera();
    }
    
    // Initialize camera for face upload page
    if (faceCaptureContainer) {
        console.log('Initializing face upload camera...');
        initFaceUploadCamera();
    }
    
    // Handle verification method switching
    const verificationMethods = document.querySelectorAll('input[name="verification_method"]');
    verificationMethods.forEach(method => {
        method.addEventListener('change', function() {
            console.log('Verification method changed to:', this.value);
            const sections = document.querySelectorAll('.verification-section');
            sections.forEach(section => section.classList.add('d-none'));
            
            const selectedSection = document.getElementById(`${this.value}-section`);
            if (selectedSection) {
                selectedSection.classList.remove('d-none');
                
                // Initialize camera if face verification is selected
                if (this.value === 'face') {
                    console.log('Face verification selected, initializing camera...');
                    setTimeout(() => {
                        initAttendanceCamera();
                    }, 100);
                }
            }
        });
    });
});

// Clean up camera when leaving page
window.addEventListener('beforeunload', function() {
    if (cameraManager) {
        cameraManager.stopCamera();
    }
});