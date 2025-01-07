from src.core.capture import ScreenCapture
from src.core.ocr import OCRProcessor
from src.core.translator import TranslationService
from src.ui.components.loading_window import LoadingWindow
from src.ui.components.overlay import TranslationOverlay
from src.utils.hotkeys import HotkeyManager
from src.config.settings import Settings
from src.utils.logger import setup_logger

def main():
    # Setup logging
    logger = setup_logger()
    logger.info("Starting...")
    
    try:
        # Show loading window
        loading = LoadingWindow()
        loading.show()
        
        # Initialize components
        settings = Settings()
        capture = ScreenCapture()
        ocr = OCRProcessor(settings.tesseract_path)
        translator = TranslationService()
        
        # Initialize main UI
        app = TranslationOverlay(capture, ocr, translator, settings)
        app.toggle_overlay()
        # Start hotkey monitoring
        hotkey_manager = HotkeyManager(app)
        hotkey_manager.start()
        
        # Close loading window and start main app
        loading.destroy()
        app.mainloop()
        
    except Exception as e:
        logger.error(f"Application startup failed: {e}")
        raise

if __name__ == "__main__":
    main()