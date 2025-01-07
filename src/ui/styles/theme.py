"""Theme configuration for the application"""

# Color scheme
COLORS = {
    'primary': '#1a1a1a',
    'secondary': '#333333',
    'accent': '#4a4a4a',
    'text': '#ffffff',
    'text_secondary': '#cccccc',
    'success': '#00ff00',
    'error': '#ff0000',
    'warning': '#ffff00'
}

# Font configurations
FONTS = {
    'main': ('Consolas', 10),
    'header': ('Consolas', 9, 'bold'),
    'small': ('Consolas', 8),
    'button': ('Consolas', 9)
}

# Loading window theme
LOADING_THEME = {
    'bg': COLORS['primary'],
    'fg': COLORS['text'],
    'font': FONTS['main']
}

# Overlay window theme
OVERLAY_THEME = {
    'window': {
        'bg': COLORS['primary'],
        'alpha': 0.8
    },
    'frame': {
        'bg': COLORS['primary'],
        'padx': 10,
        'pady': 10
    },
    'label': {
        'bg': COLORS['primary'],
        'fg': COLORS['text'],
        'font': FONTS['main']
    },
    'header': {
        'bg': COLORS['primary'],
        'fg': COLORS['text'],
        'font': FONTS['header']
    },
    'entry': {
        'bg': COLORS['secondary'],
        'fg': COLORS['text'],
        'insertbackground': COLORS['text'],
        'font': FONTS['main'],
        'relief': 'flat'
    },
    'button': {
        'bg': COLORS['accent'],
        'fg': COLORS['text'],
        'font': FONTS['button'],
        'relief': 'flat',
        'activebackground': COLORS['secondary']
    },
    'button_danger': {
        'bg': COLORS['error'],
        'fg': COLORS['text'],
        'font': FONTS['button'],
        'relief': 'flat'
    }
}