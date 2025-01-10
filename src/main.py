from src.core.capture import ScreenCapture
from src.core.ocr import OCRProcessor
from src.core.translator import TranslationService
from src.core.openai import OpenAIChatAnalyzer
from src.ui.components.overlay import TranslationOverlay
from src.utils.hotkeys import HotkeyManager
from src.config.settings import Settings
from src.utils.logger import setup_logger

OPEN_ROUTER_API_KEY=""

def main():
    logger = setup_logger()
    logger.info("Starting...")
    
    try:
        settings = Settings()
        capture = ScreenCapture()
        ocr = OCRProcessor(settings.tesseract_path)
        translator = TranslationService()
        analyzer = OpenAIChatAnalyzer(OPEN_ROUTER_API_KEY, dev_mode=False)
        
        app = TranslationOverlay(capture, ocr, translator, analyzer, settings)
        app.toggle_overlay()
        hotkey_manager = HotkeyManager(app)
        hotkey_manager.start()
        
        app.mainloop()
        
    except Exception as e:
        logger.error(f"Application startup failed: {e}")
        raise

if __name__ == "__main__":
    main()