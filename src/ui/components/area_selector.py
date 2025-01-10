import tkinter as tk
from typing import Optional, Callable, Dict, Coroutine, Any
import logging

logger = logging.getLogger(__name__)

class AreaSelector(tk.Toplevel):
    def __init__(
        self,
        parent: tk.Tk,
        callback: Callable[[Optional[Dict[str, int]]], Coroutine[Any, Any, None]]
    ):
        super().__init__(parent)
        
        self.parent = parent
        self.callback = callback
        self.setup_window()
        self.setup_canvas()
        self.bind_events()
        
        self.focus_force()
        self.lift()
        self.attributes('-topmost', True)
    
    def setup_window(self):
        """Setup window properties"""
        self.attributes('-fullscreen', True, '-alpha', 0.3, '-topmost', True)
        self.configure(bg='black')
        
        self.state('normal')
        self.focus_set()
    
    def setup_canvas(self):
        """Setup canvas for area selection"""
        self.canvas = tk.Canvas(
            self,
            highlightthickness=0,
            bg='black'
        )
        self.canvas.pack(fill='both', expand=True)
        
        self.canvas.create_text(
            self.winfo_screenwidth() // 2,
            50,
            text="Click and drag to select the area to translate\nPress ESC to cancel",
            fill='white',
            font=('Arial', 24),
            justify='center'
        )
        
        self.start_x = None
        self.start_y = None
        self.current_rect = None
    
    def bind_events(self):
        """Bind mouse and keyboard events"""
        self.canvas.bind('<Button-1>', self.start_selection)
        self.canvas.bind('<B1-Motion>', self.update_selection)
        self.canvas.bind('<ButtonRelease-1>', self.end_selection)
        self.bind('<Escape>', self.cancel_selection)
    
    def start_selection(self, event):
        """Handle selection start"""
        self.start_x = event.x
        self.start_y = event.y
        if self.current_rect:
            self.canvas.delete(self.current_rect)
    
    def update_selection(self, event):
        """Update selection rectangle"""
        if self.current_rect:
            self.canvas.delete(self.current_rect)
        self.current_rect = self.canvas.create_rectangle(
            self.start_x, self.start_y,
            event.x, event.y,
            outline='red',
            width=2
        )
    
    def _invoke_callback(self, area: Optional[Dict[str, int]]):
        """Invoke the async callback"""
        if hasattr(self.parent, 'async_helper'):
            self.parent.async_helper.run_coroutine(self.callback(area))
        else:
            logger.error("Parent window does not have async_helper")
    
    def end_selection(self, event):
        """Handle selection end"""
        try:
            x1, y1 = min(self.start_x, event.x), min(self.start_y, event.y)
            x2, y2 = max(self.start_x, event.x), max(self.start_y, event.y)
            
            selected_area = {
                'left': int(x1),
                'top': int(y1),
                'width': int(x2 - x1),
                'height': int(y2 - y1)
            }
            
            self.withdraw()
            if self.callback:
                self._invoke_callback(selected_area)
        except Exception as e:
            logger.error(f"Error in end_selection: {e}")
    
    def cancel_selection(self, event):
        """Cancel selection"""
        self.withdraw()
        if self.callback:
            self._invoke_callback(None)