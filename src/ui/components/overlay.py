import tkinter as tk
from tkinter import ttk
import logging
import queue
import asyncio
from src.config.constants import AVAILABLE_LANGUAGES
from src.ui.styles.theme import OVERLAY_THEME, FONTS, COLORS
from src.core.capture import ScreenCapture
from src.core.ocr import OCRProcessor
from src.core.openai import OpenAIChatAnalyzer
from src.core.translator import TranslationService
from src.config.settings import Settings
from src.ui.components.area_selector import AreaSelector

logger = logging.getLogger(__name__)

class AsyncTkHelper:
    """Helper class to run async tasks in Tkinter"""
    def __init__(self, root: tk.Tk):
        self.root = root
        self.loop = None
        self._setup_async_loop()

    def _setup_async_loop(self):
        """Set up the async event loop"""
        # Get or create event loop
        try:
            self.loop = asyncio.get_event_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

    async def run_async(self, coro):
        """Run an async coroutine and return its result"""
        return await coro

    def run_coroutine(self, coro):
        """Schedule a coroutine to run in the event loop"""
        asyncio.run_coroutine_threadsafe(coro, self.loop)

    def process_async(self):
        """Process async events"""
        self.loop.call_soon(self.loop.stop)
        self.loop.run_forever()
        self.root.after(50, self.process_async)

class TranslationOverlay(tk.Tk):
    def __init__(
        self,
        capture: ScreenCapture,
        ocr: OCRProcessor,
        translator: TranslationService,
        chat_analyzer: OpenAIChatAnalyzer,
        settings: Settings
    ):
        super().__init__()
        
        # Initialize async helper
        self.async_helper = AsyncTkHelper(self)
        
        # Store dependencies
        self.capture = capture
        self.ocr = ocr
        self.chat_analyzer = chat_analyzer
        self.translator = translator
        self.settings = settings
        
        # Initialize queues
        self.command_queue = queue.Queue()
        self.result_queue = queue.Queue()
        
        # Setup window properties
        self.setup_window()
        
        # Setup UI components
        self.setup_ui()
        
        # Start checking command queue
        self.check_command_queue()
        
        # Start processing async events
        self.async_helper.process_async()
        
    def setup_window(self):
        """Configure main window properties"""
        self.withdraw()  # Hide window initially
        self.overrideredirect(True)  # Remove window decorations
        self.attributes("-topmost", True)  # Keep on top
        self.attributes("-alpha", OVERLAY_THEME['window']['alpha'])
        self.configure(bg=OVERLAY_THEME['window']['bg'])
        
        # Position window
        self.geometry("+100+100")  # Initial position
        
    def setup_ui(self):
        """Setup all UI components"""
        # Main container
        self.main_frame = tk.Frame(
            self,
            bg=OVERLAY_THEME['frame']['bg'],
            padx=OVERLAY_THEME['frame']['padx'],
            pady=OVERLAY_THEME['frame']['pady']
        )
        self.main_frame.pack(fill='both', expand=True)
        
        # Instructions
        self.setup_instructions()
        
        # Translation section
        self.setup_translation_section()
        
        # Input section
        self.setup_input_section()
        
        # Buttons
        self.setup_buttons()
        
        # Version label
        self.setup_version_label()
        
        # Make entire window draggable by binding to all frames
        for widget in (self.main_frame, self.translation_frame, self.input_frame):
            widget.bind("<Button-1>", self.start_drag)
            widget.bind("<B1-Motion>", self.do_drag)
            
        # Make labels draggable
        for widget in (self.instructions, self.translation_text):
            widget.bind("<Button-1>", self.start_drag)
            widget.bind("<B1-Motion>", self.do_drag)

    def setup_version_label(self):
        """Setup version label in bottom right"""
        version_label_config = OVERLAY_THEME['label'].copy()
        version_label_config['font'] = FONTS['small']
        version_label_config['fg'] = COLORS['text_secondary']
        
        version_frame = tk.Frame(
            self.main_frame,
            bg=OVERLAY_THEME['frame']['bg']
        )
        version_frame.pack(fill='x', pady=(5, 0))
        
        version_text = f"v{self.settings.version}"
        version_label = tk.Label(
            version_frame,
            text=version_text,
            **version_label_config
        )
        version_label.pack(side='right')
        
        # Make version label draggable
        version_label.bind("<Button-1>", self.start_drag)
        version_label.bind("<B1-Motion>", self.do_drag)
    
    def setup_instructions(self):
        """Setup instructions label"""
        instructions_text = (
            "Press Ctrl+Alt+X to select area and translate\n"
            "Ctrl+Alt+C to toggle overlay"
        )
        
        # Create a copy of the label theme and override the font and color
        label_config = OVERLAY_THEME['label'].copy()
        label_config['font'] = FONTS['small']
        label_config['fg'] = COLORS['text_secondary']  # Set to gray color
        
        self.instructions = tk.Label(
            self.main_frame,
            text=instructions_text,
            **label_config
        )
        self.instructions.pack(anchor='w', pady=(0, 10))
    
    def setup_translation_section(self):
        """Setup the translation display area"""
        # Translation frame
        self.translation_frame = tk.Frame(
            self.main_frame,
            bg=OVERLAY_THEME['frame']['bg']
        )
        self.translation_frame.pack(fill='x', pady=(0, 10))
        
        # Header
        header_frame = tk.Frame(
            self.translation_frame,
            bg=OVERLAY_THEME['frame']['bg']
        )
        header_frame.pack(fill='x')
        
        tk.Label(
            header_frame,
            text="Translated text:",
            **OVERLAY_THEME['header']
        ).pack(side='left')
        
        # Code block style frame for translation
        translation_block = tk.Frame(
            self.translation_frame,
            bg=COLORS['secondary'],  # Slightly lighter background
        )
        translation_block.pack(fill='x', pady=5)
        
        # Add padding frame inside
        padding_frame = tk.Frame(
            translation_block,
            bg=COLORS['secondary']
        )
        padding_frame.pack(fill='x', padx=10, pady=10)
        
        # Translation display with code-block styling
        self.translation_text = tk.Label(
            padding_frame,
            text="No translation yet",
            wraplength=300,
            justify='left',
            bg=COLORS['secondary'],
            fg=COLORS['text'],
            font=FONTS['main']
        )
        self.translation_text.pack(fill='x')
    
    def setup_input_section(self):
        """Setup input and translation entry fields"""
        # Input frame
        self.input_frame = tk.Frame(
            self.main_frame,
            bg=OVERLAY_THEME['frame']['bg']
        )
        self.input_frame.pack(fill='x', pady=(0, 10))
        
        # English input
        tk.Label(
            self.input_frame,
            text="Your message (EN):",
            **OVERLAY_THEME['header']
        ).pack(anchor='w')
        
        self.input_field = tk.Entry(
            self.input_frame,
            **OVERLAY_THEME['entry']
        )
        self.input_field.pack(fill='x', pady=(5, 10))
        # Bind Enter key to translate
        self.input_field.bind('<Return>', lambda event: self.translate_input())
        
        # Translation target section
        self.setup_translation_target()
    
    def setup_translation_target(self):
        """Setup translation target language selection"""
        target_frame = tk.Frame(
            self.input_frame,
            bg=OVERLAY_THEME['frame']['bg']
        )
        target_frame.pack(fill='x')
        
        # Create modified theme for small text label
        label_config = OVERLAY_THEME['label'].copy()
        label_config['font'] = FONTS['small']
        
        tk.Label(
            target_frame,
            text="Translate to:",
            **label_config
        ).pack(side='left')
        
        self.target_lang = ttk.Combobox(
            target_frame,
            values=list(AVAILABLE_LANGUAGES.keys()),
            width=15,
            state='readonly',
            font=FONTS['small']
        )
        self.target_lang.set('Portuguese')
        self.target_lang.pack(side='right')

        # Result container frame
        result_container = tk.Frame(
            self.input_frame,
            bg=OVERLAY_THEME['frame']['bg']
        )
        result_container.pack(fill='x', pady=(5, 0))
        
        # Result field
        entry_config = OVERLAY_THEME['entry'].copy()
        entry_config['fg'] = COLORS['success']  # Override text color to green
        self.result_field = tk.Entry(
            result_container,
            **entry_config,
            state='readonly',
            readonlybackground=OVERLAY_THEME['entry']['bg']
        )
        self.result_field.pack(side='left', fill='x', expand=True)
        
        # Copy button
        self.copy_button = tk.Button(
            result_container,
            text="📋",
            command=self.copy_translation,
            **OVERLAY_THEME['button'],
            width=3,
            padx=2
        )
        self.copy_button.pack(side='left', padx=(5, 0))
    
    def setup_buttons(self):
        """Setup control buttons"""
        button_frame = tk.Frame(
            self.main_frame,
            bg=OVERLAY_THEME['frame']['bg']
        )
        button_frame.pack(fill='x', pady=(10, 0))
        
        # Left side buttons
        tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_fields,
            **OVERLAY_THEME['button']
        ).pack(side='left', padx=(0, 5))
        
        tk.Button(
            button_frame,
            text="Exit",
            command=self.quit_app,
            **OVERLAY_THEME['button_danger']
        ).pack(side='left')
        
        # Right side buttons
        tk.Button(
            button_frame,
            text="Translate",
            command=self.translate_input,
            **OVERLAY_THEME['button']
        ).pack(side='right')
    
    def copy_translation(self):
        """Copy translation to clipboard"""
        translation = self.result_field.get()
        if translation and not translation.startswith('Error:'):
            self.clipboard_clear()
            self.clipboard_append(translation)
            
            # Visual feedback - temporarily change button color
            original_bg = self.copy_button.cget('bg')
            self.copy_button.configure(bg=OVERLAY_THEME['button_danger']['bg'])
            self.after(200, lambda: self.copy_button.configure(bg=original_bg))

    def start_drag(self, event):
        """Start window drag"""
        self._drag_start_x = event.x
        self._drag_start_y = event.y
    
    def do_drag(self, event):
        """Handle window dragging"""
        x = self.winfo_x() + (event.x - self._drag_start_x)
        y = self.winfo_y() + (event.y - self._drag_start_y)
        self.geometry(f"+{x}+{y}")
    
    def check_command_queue(self):
        """Process commands from queue"""
        try:
            while True:
                command = self.command_queue.get_nowait()
                if command == 'select_area':
                    self.start_area_selection()
                elif command == 'toggle_overlay':
                    self.toggle_overlay()
                elif command == 'clear_fields':
                    self.clear_fields()
        except queue.Empty:
            pass
        finally:
            self.after(100, self.check_command_queue)
    
    def start_area_selection(self):
        """Start area selection process"""
        self.withdraw()
        selector = AreaSelector(self, self.handle_area_selection)
        selector.deiconify()
    
    async def handle_area_selection(self, area):
        """Handle selected area"""
        if area:
            try:
                # Capture and process image                
                chat_image = self.capture.capture_area(area)
                text = self.ocr.process_image(chat_image)
                result = await self.chat_analyzer.analyze_text_only(text)
                
                # Schedule UI updates in the main thread
                self.after(0, lambda: self._update_translation(result))
            except Exception as e:
                logger.error(f"Translation failed: {e}")
                self.after(0, lambda: self._update_translation(f"Error: {str(e)}"))
    
    def _update_translation(self, result: str):
        """Update translation UI in the main thread"""
        self.translation_text.config(text=result)
        self.deiconify()
    
    def toggle_overlay(self):
        """Toggle overlay visibility"""
        if self.state() == 'withdrawn':
            self.deiconify()
        else:
            self.withdraw()
    
    def clear_fields(self):
        """Clear all input fields"""
        self.input_field.delete(0, tk.END)
        self.result_field.config(state='normal')
        self.result_field.delete(0, tk.END)
        self.result_field.config(state='readonly')
    
    def translate_input(self):
        """Translate input text"""
        text = self.input_field.get().strip()
        if text:
            try:
                target = AVAILABLE_LANGUAGES[self.target_lang.get()]
                result = self.translator.translate(text, target)
                
                self.result_field.config(state='normal')
                self.result_field.delete(0, tk.END)
                self.result_field.insert(0, result['translation'])
                self.result_field.config(state='readonly')
            except Exception as e:
                logger.error(f"Translation failed: {e}")
                self.result_field.config(state='normal')
                self.result_field.delete(0, tk.END)
                self.result_field.insert(0, f"Error: {str(e)}")
                self.result_field.config(state='readonly')
    
    def quit_app(self):
        """Exit application"""
        self.capture.cleanup()
        self.quit()