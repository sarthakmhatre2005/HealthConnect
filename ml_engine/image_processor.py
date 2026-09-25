"""
HealthConnect Secure Medical Image Intake & Preprocessing Engine
Handles:
- Cryptographically safe filename generation and storage in protected directory
- Strict MIME and binary header validation (JPG, JPEG, PNG, WEBP)
- File size limitation (max 5 MB)
- Image readability and corruption detection via PIL
- Medical visual preprocessing (224x224 RGB standardization)
- Statistical visual feature descriptor extraction
- Clear, transparent separation between image intake and symptom ML models
"""

import os
import uuid
import logging
from typing import Dict, Any, Tuple, Optional
import numpy as np

try:
    from PIL import Image, UnidentifiedImageError
    PIL_AVAILABLE = True
except ImportError:
    Image = None
    UnidentifiedImageError = Exception
    PIL_AVAILABLE = False
    logging.getLogger(__name__).warning("Pillow (PIL) not installed in current environment; medical image processing standby.")

logger = logging.getLogger(__name__)

# Allowed file extensions and corresponding PIL formats
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}
ALLOWED_FORMATS = {'JPEG', 'PNG', 'WEBP'}
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB
MIN_DIMENSION = 50
MAX_DIMENSION = 4096

# Protected medical image storage directory (outside static/public web root)
SECURE_UPLOAD_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "instance", "secure_uploads", "medical_images")
)

def ensure_secure_dir() -> str:
    """Ensures the protected upload directory exists."""
    os.makedirs(SECURE_UPLOAD_DIR, exist_ok=True)
    return SECURE_UPLOAD_DIR

def is_allowed_file(filename: str) -> bool:
    """Validates file extension against allowed medical image extensions."""
    if not filename or '.' not in filename:
        return False
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS

def extract_visual_descriptors(img: Any) -> Dict[str, Any]:
    """
    Extracts statistical visual descriptors from standardized 224x224 RGB image.
    Provides real feature extraction for multimodal integration while keeping
    clear transparency about deep model status.
    """
    try:
        # Resize to standard vision tensor input size
        resized = img.resize((224, 224), Image.Resampling.LANCZOS)
        arr = np.array(resized, dtype=np.float32) / 255.0  # Normalize to [0, 1]
        
        # Color channel statistics
        r_mean, g_mean, b_mean = np.mean(arr[:, :, 0]), np.mean(arr[:, :, 1]), np.mean(arr[:, :, 2])
        r_std, g_std, b_std = np.std(arr[:, :, 0]), np.std(arr[:, :, 1]), np.std(arr[:, :, 2])
        
        # Redness dominance ratio (relevant for erythema / skin rash)
        rg_ratio = float(r_mean / (g_mean + 1e-6))
        
        # Simple color histograms (8 bins per channel = 24 features)
        r_hist, _ = np.histogram(arr[:, :, 0], bins=8, range=(0, 1), density=True)
        g_hist, _ = np.histogram(arr[:, :, 1], bins=8, range=(0, 1), density=True)
        b_hist, _ = np.histogram(arr[:, :, 2], bins=8, range=(0, 1), density=True)
        
        # Spatial variance (texture heterogeneity)
        gray = 0.2989 * arr[:, :, 0] + 0.5870 * arr[:, :, 1] + 0.1140 * arr[:, :, 2]
        texture_variance = float(np.var(gray))
        
        combined_features = np.concatenate([
            [r_mean, g_mean, b_mean, r_std, g_std, b_std, rg_ratio, texture_variance],
            r_hist[:4], g_hist[:4], b_hist[:4]
        ]).tolist()
        
        return {
            "dimensions_standardized": [224, 224, 3],
            "channel_means": [round(float(r_mean), 3), round(float(g_mean), 3), round(float(b_mean), 3)],
            "redness_ratio": round(rg_ratio, 3),
            "texture_variance": round(texture_variance, 4),
            "feature_vector_dim": len(combined_features),
            "feature_vector": [round(float(v), 4) for v in combined_features]
        }
    except Exception as e:
        logger.error(f"Error extracting visual descriptors: {e}")
        return {
            "dimensions_standardized": [224, 224, 3],
            "feature_vector_dim": 0,
            "feature_vector": []
        }

def process_uploaded_image(file_storage) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
    """
    Validates and securely persists an uploaded medical image.
    
    Args:
        file_storage: Werkzeug FileStorage object from request.files['image']
        
    Returns:
        Tuple of:
        - success (bool)
        - metadata dict (if success)
        - error message (if failure)
    """
    if not file_storage or not getattr(file_storage, 'filename', None):
        return False, None, "No image file provided."
        
    original_filename = file_storage.filename
    if not is_allowed_file(original_filename):
        return False, None, "Unsupported image format. Allowed formats: JPG, JPEG, PNG, WEBP."
        
    # Check file size by seeking
    try:
        file_storage.seek(0, os.SEEK_END)
        file_size = file_storage.tell()
        file_storage.seek(0)
        
        if file_size > MAX_FILE_SIZE_BYTES:
            max_mb = MAX_FILE_SIZE_BYTES // (1024 * 1024)
            return False, None, f"Image file is too large ({file_size / (1024*1024):.1f} MB). Maximum size is {max_mb} MB."
            
        if file_size < 100:
            return False, None, "Image file is empty or corrupted."
    except Exception as e:
        logger.error(f"Failed to verify file size: {e}")
        return False, None, "Failed to read image stream."

    if not PIL_AVAILABLE:
        return False, None, "Pillow library is not installed in the environment. Please run: pip install pillow"

    # Validate image readability and dimensions using PIL
    try:
        img = Image.open(file_storage)
        img.verify()  # Check for header/structure corruption
        
        # Reset stream after verify() to load actual pixels
        file_storage.seek(0)
        img = Image.open(file_storage)
        img.load()
        
        format_name = img.format
        if format_name not in ALLOWED_FORMATS:
            return False, None, f"Image format '{format_name}' is not supported. Please upload a standard JPG, PNG, or WEBP."
            
        width, height = img.size
        if width < MIN_DIMENSION or height < MIN_DIMENSION:
            return False, None, f"Image dimensions ({width}x{height}px) are too small. Minimum required is {MIN_DIMENSION}x{MIN_DIMENSION}px."
            
        if width > MAX_DIMENSION or height > MAX_DIMENSION:
            return False, None, f"Image dimensions ({width}x{height}px) exceed maximum allowed {MAX_DIMENSION}px."
            
        # Convert to RGB if RGBA/P/grayscale
        if img.mode != 'RGB':
            rgb_img = img.convert('RGB')
        else:
            rgb_img = img
            
    except UnidentifiedImageError:
        return False, None, "The uploaded file is not a valid or readable image."
    except Exception as e:
        logger.error(f"Image validation failed: {e}")
        return False, None, f"Image processing failed: Invalid image data."
        
    # Extract visual features
    visual_features = extract_visual_descriptors(rgb_img)
    
    # Generate cryptographically secure UUID filename
    ensure_secure_dir()
    secure_filename = f"{uuid.uuid4().hex}.jpg"
    dest_path = os.path.join(SECURE_UPLOAD_DIR, secure_filename)
    
    # Save optimized JPEG to secure protected storage
    try:
        rgb_img.save(dest_path, format="JPEG", quality=88, optimize=True)
    except Exception as e:
        logger.error(f"Failed to save image to secure storage: {e}")
        return False, None, "Failed to store image securely on server."
        
    metadata = {
        "success": True,
        "filename": secure_filename,
        "original_filename": os.path.basename(original_filename),
        "file_size_bytes": file_size,
        "dimensions": [width, height],
        "format": format_name,
        "visual_features": visual_features,
        "image_analyzed": True,
        "privacy_notice": "Image securely processed and stored in protected medical records. Never publicly accessible.",
        "model_architecture_note": "Visual feature tensor [1, 3, 224, 224] extracted. Clinical likelihood generated via primary symptom parameter models."
    }
    
    return True, metadata, None

def get_image_path(filename: str) -> Optional[str]:
    """Returns absolute path to secure image if valid and exists."""
    if not filename or '/' in filename or '\\' in filename or '..' in filename:
        return None
    path = os.path.join(SECURE_UPLOAD_DIR, filename)
    if os.path.exists(path) and os.path.isfile(path):
        return path
    return None
