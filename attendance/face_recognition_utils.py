import cv2
import numpy as np
import os
import pickle
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import base64
from io import BytesIO
from PIL import Image

# Directory to store face encodings
FACE_ENCODINGS_DIR = os.path.join(settings.MEDIA_ROOT, 'face_encodings')

def ensure_face_encodings_dir():
    """Ensure the face encodings directory exists"""
    if not os.path.exists(FACE_ENCODINGS_DIR):
        os.makedirs(FACE_ENCODINGS_DIR)

def process_uploaded_image(image_file):
    """Process uploaded image and return numpy array"""
    try:
        # Read image file
        image_data = image_file.read()
        image_file.seek(0)  # Reset file pointer
        
        # Convert to numpy array
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        return image
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def detect_faces(image_array):
    """Detect faces in the image using OpenCV"""
    try:
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        
        # Load the face cascade classifier
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # Convert to list of tuples (top, right, bottom, left)
        face_locations = []
        for (x, y, w, h) in faces:
            face_locations.append((y, x + w, y + h, x))
        
        return face_locations
    except Exception as e:
        print(f"Error detecting faces: {e}")
        return []

def extract_face_features(image_array, face_locations):
    """Extract face features using basic image processing"""
    try:
        features = []
        for face_location in face_locations:
            top, right, bottom, left = face_location
            
            # Extract face region
            face_image = image_array[top:bottom, left:right]
            
            # Resize to standard size
            face_image = cv2.resize(face_image, (128, 128))
            
            # Convert to grayscale
            gray_face = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
            
            # Normalize
            normalized_face = gray_face / 255.0
            
            # Flatten to 1D array
            face_features = normalized_face.flatten()
            
            features.append(face_features)
        
        return features
    except Exception as e:
        print(f"Error extracting face features: {e}")
        return []

def save_face_encoding(user, face_features):
    """Save face features for a user"""
    try:
        ensure_face_encodings_dir()
        
        # Save features as pickle file
        encoding_file = os.path.join(FACE_ENCODINGS_DIR, f'user_{user.id}_encoding.pkl')
        with open(encoding_file, 'wb') as f:
            pickle.dump(face_features, f)
        
        return True
    except Exception as e:
        print(f"Error saving face encoding: {e}")
        return False

def load_face_encoding(user):
    """Load face features for a user"""
    try:
        encoding_file = os.path.join(FACE_ENCODINGS_DIR, f'user_{user.id}_encoding.pkl')
        if os.path.exists(encoding_file):
            with open(encoding_file, 'rb') as f:
                return pickle.load(f)
        return None
    except Exception as e:
        print(f"Error loading face encoding: {e}")
        return None

def compare_faces(features1, features2, threshold=0.8):
    """Compare two face feature vectors using cosine similarity"""
    try:
        # Calculate cosine similarity
        dot_product = np.dot(features1, features2)
        norm1 = np.linalg.norm(features1)
        norm2 = np.linalg.norm(features2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        return similarity
    except Exception as e:
        print(f"Error comparing faces: {e}")
        return 0.0

def verify_face(user, captured_face_features, threshold=0.7):
    """Verify if the captured face matches the stored face"""
    try:
        stored_features = load_face_encoding(user)
        if stored_features is None:
            return False, 0.0, "No stored face features found"
        
        # Compare face features
        similarity = compare_faces(stored_features, captured_face_features)
        
        if similarity >= threshold:
            return True, similarity, f"Face verified with {similarity:.2%} confidence"
        else:
            return False, similarity, f"Face does not match. Similarity: {similarity:.2%}"
            
    except Exception as e:
        print(f"Error verifying face: {e}")
        return False, 0.0, f"Error during face verification: {str(e)}"

def process_camera_image(image_data_url):
    """Process image data URL from camera capture"""
    try:
        # Remove data URL prefix
        if image_data_url.startswith('data:image/'):
            # Extract base64 data
            header, data = image_data_url.split(',', 1)
            image_data = base64.b64decode(data)
            
            # Convert to numpy array
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            return image
        else:
            return None
    except Exception as e:
        print(f"Error processing camera image: {e}")
        return None

def capture_and_verify_face(user, image_data_url):
    """Capture face from camera and verify against stored features"""
    try:
        # Process the captured image
        image_array = process_camera_image(image_data_url)
        if image_array is None:
            return False, 0.0, "Could not process captured image"
        
        # Detect faces
        face_locations = detect_faces(image_array)
        if not face_locations:
            return False, 0.0, "No face detected in the image"
        
        if len(face_locations) > 1:
            return False, 0.0, "Multiple faces detected. Please ensure only one face is visible"
        
        # Extract face features
        face_features = extract_face_features(image_array, face_locations)
        if not face_features:
            return False, 0.0, "Could not extract facial features"
        
        # Verify face
        is_match, confidence, message = verify_face(user, face_features[0])
        
        return is_match, confidence, message
        
    except Exception as e:
        print(f"Error in capture_and_verify_face: {e}")
        return False, 0.0, f"Error during face verification: {str(e)}"

def get_face_recognition_status(user):
    """Check if user has face recognition enabled"""
    try:
        encoding_file = os.path.join(FACE_ENCODINGS_DIR, f'user_{user.id}_encoding.pkl')
        return os.path.exists(encoding_file)
    except Exception as e:
        print(f"Error checking face recognition status: {e}")
        return False

def delete_face_encoding(user):
    """Delete face encoding for a user"""
    try:
        encoding_file = os.path.join(FACE_ENCODINGS_DIR, f'user_{user.id}_encoding.pkl')
        if os.path.exists(encoding_file):
            os.remove(encoding_file)
            return True
        return False
    except Exception as e:
        print(f"Error deleting face encoding: {e}")
        return False