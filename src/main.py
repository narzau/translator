from src.core.capture import ScreenCapture
from src.core.ocr import OCRProcessor
from src.core.translator import TranslationService
from src.core.openai import OpenAIChatAnalyzer
from src.ui.components.loading_window import LoadingWindow
from src.ui.components.overlay import TranslationOverlay
from src.utils.hotkeys import HotkeyManager
from src.config.settings import Settings
from src.utils.logger import setup_logger

OPEN_ROUTER_API_KEY="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"

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
        analyzer = OpenAIChatAnalyzer(OPEN_ROUTER_API_KEY, dev_mode=False)
        
        # Initialize main UI
        app = TranslationOverlay(capture, ocr, translator, analyzer, settings)
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