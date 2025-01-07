from PIL import Image
import cv2
import numpy as np
import pytesseract
import logging
from typing import Optional
from datetime import datetime
from src.config.constants import OCR_CONFIG, DEBUG_DIR
from src.utils.image_processing import preprocess_image

logger = logging.getLogger(__name__)

class OCRProcessor:
    def __init__(self, tesseract_path: str):
        self.tesseract_path = tesseract_path
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
    def process_image(self, image: Image.Image, save_debug: bool = False) -> str:
        """
        Process image and extract text
        
        Args:
            image: PIL Image to process
            save_debug: Whether to save debug images
            
        Returns:
            Extracted text from the image
        """
        try:
            processed_image = preprocess_image(image, save_debug)
            return self._extract_text(processed_image)
        except Exception as e:
            logger.error(f"OCR processing failed: {e}")
            raise
    
    def _extract_text(self, image: Image.Image) -> str:
        """Extract text from processed image"""
        text = pytesseract.image_to_string(
            image,
            lang='por',
            config=OCR_CONFIG
        )
        
        # Clean and reconstruct messages
        lines = text.split('\n')
        cleaned_lines = []
        temp_message = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if ':' in line:
                if temp_message:
                    cleaned_lines.append(' '.join(temp_message))
                    temp_message = []
                temp_message = [line]
            elif temp_message:
                temp_message.append(line)
            else:
                temp_message = [line]
        
        if temp_message:
            cleaned_lines.append(' '.join(temp_message))
        
        return '\n'.join(cleaned_lines)