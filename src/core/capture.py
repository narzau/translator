from typing import Dict
import mss
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class ScreenCapture:
    def __init__(self):
        self.screen_capture = mss.mss()
    
    def capture_area(self, area: Dict[str, int]) -> Image.Image:
        """
        Capture a specific area of the screen
        
        Args:
            area: Dictionary with left, top, width, height keys
            
        Returns:
            PIL Image of the captured area
        """
        try:
            screenshot = self.screen_capture.grab(area)
            return Image.frombytes('RGB', screenshot.size, screenshot.rgb)
        except Exception as e:
            logger.error(f"Screen capture failed: {e}")
            raise

    def cleanup(self):
        """Clean up resources"""
        self.screen_capture.close()