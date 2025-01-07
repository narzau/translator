# src/ui/components/loading_window.py
import tkinter as tk
from src.ui.styles.theme import LOADING_THEME

class LoadingWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_ui()
        # Initially withdraw the window until we're ready to show it
        self.withdraw()
    
    def setup_window(self):
        """Setup window properties"""
        self.title("Loading")
        self.geometry("300x100")
        self.configure(bg=LOADING_THEME['bg'])
        self.attributes('-topmost', True)
        
        # Center window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 300) // 2
        y = (screen_height - 100) // 2
        self.geometry(f"300x100+{x}+{y}")
    
    def setup_ui(self):
        """Setup UI components"""
        self.label = tk.Label(
            self,
            text="Starting...",
            bg=LOADING_THEME['bg'],
            fg=LOADING_THEME['fg'],
            font=LOADING_THEME['font']
        )
        self.label.pack(expand=True)
    
    def show(self):
        """Show the loading window"""
        self.deiconify()
    
    def update_status(self, text: str):
        """Update loading status"""
        self.label.config(text=text)