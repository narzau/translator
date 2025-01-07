"""Image processing utilities"""
from PIL import Image
import cv2
import numpy as np
from datetime import datetime
import os
from src.config.constants import DEBUG_DIR
import logging

logger = logging.getLogger(__name__)

def preprocess_image(image: Image.Image, save_debug: bool = False) -> Image.Image:
    """
    Preprocess image for better OCR results
    
    Args:
        image: PIL Image to process
        save_debug: Whether to save debug images
        
    Returns:
        Processed PIL Image
    """
    try:
        # Convert to numpy array
        np_image = np.array(image)
        
        # Convert to grayscale
        gray = cv2.cvtColor(np_image, cv2.COLOR_RGB2GRAY)
        
        # Apply threshold
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Find text contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Create mask for text
        mask = np.zeros_like(binary)
        for contour in contours:
            cv2.drawContours(mask, [contour], -1, (255, 255, 255), -1)
        
        # Apply mask
        result = cv2.bitwise_and(binary, mask)
        
        # Invert to black text on white background
        result = cv2.bitwise_not(result)
        
        # Add white border
        result = cv2.copyMakeBorder(result, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=255)
        
        # Scale up
        result = cv2.resize(result, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        
        if save_debug:
            save_debug_images(np_image, result)
        
        return Image.fromarray(result)
        
    except Exception as e:
        logger.error(f"Image preprocessing failed: {e}")
        raise