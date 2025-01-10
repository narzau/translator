"""Hotkey management"""
import keyboard
import threading
import time
import logging
from src.config.constants import HOTKEYS

logger = logging.getLogger(__name__)

class HotkeyManager:
    def __init__(self, app):
        self.app = app
        self.running = False
        self.thread = None
    
    def start(self):
        """Start hotkey monitoring"""
        self.running = True
        self.thread = threading.Thread(target=self._monitor_hotkeys)
        self.thread.daemon = True
        self.thread.start()
        logger.info("Hotkey monitoring started")
    
    def stop(self):
        """Stop hotkey monitoring"""
        self.running = False
        if self.thread:
            self.thread.join()
        logger.info("Hotkey monitoring stopped")
    
    def _monitor_hotkeys(self):
        """Monitor for hotkey presses"""
        while self.running:
            try:
                if keyboard.is_pressed(HOTKEYS['select_area']):
                    self.app.command_queue.put('select_area')
                    time.sleep(0.3)
                elif keyboard.is_pressed(HOTKEYS['toggle_overlay']):
                    self.app.command_queue.put('toggle_overlay')
                    time.sleep(0.3)
                elif keyboard.is_pressed(HOTKEYS['clear_fields']):
                    self.app.command_queue.put('clear_fields')
                    time.sleep(0.3)
                elif keyboard.is_pressed(HOTKEYS['copy_translation']):
                    self.app.command_queue.put('copy_translation')
                    time.sleep(0.3)
            except Exception as e:
                logger.error(f"Error in hotkey monitoring: {e}")
            time.sleep(0.1)
