# Live Screen Translator

A real-time screen translation tool that captures text from any area of your screen and translates it on the fly. Perfect for games, applications, or any scenario where you need instant translation of text that appears on your screen.

## Features

- Real-time screen area capture and translation
- Support for multiple languages
- Draggable, semi-transparent overlay
- Two-way translation capability:
  - Capture and translate text from screen
  - Translate your own text for communication
- Global hotkeys for quick access
- Customizable translation area selection

## Use Cases

- Gaming with international players
- Reading foreign language content
- International software usage
- Live chat translation
- Learning new languages

## How to Set Up

### Prerequisites

1. Python 3.8 or higher
2. Tesseract OCR

### Installation Steps

1. **Clone or download this repository**
   ```bash
   git clone https://github.com/yourusername/live-screen-translator.git
   cd live-screen-translator
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Tesseract OCR**
   
   Windows:
   - Download installer from https://github.com/UB-Mannheim/tesseract/wiki
   - Install to `C:\Program Files\Tesseract-OCR`
   - Add to PATH: `C:\Program Files\Tesseract-OCR`

   Linux:
   ```bash
   sudo apt-get update
   sudo apt-get install tesseract-ocr
   sudo apt-get install tesseract-ocr-por  # For Portuguese
   ```

   Mac:
   ```bash
   brew install tesseract
   brew install tesseract-lang  # Language packs
   ```

### Running the Application

1. **From the project directory, with virtual environment activated:**
   ```bash
   python run.py
   ```

2. **Using the application:**
   - Press `Ctrl+Alt+X` to select the area you want to translate
   - Press `Ctrl+Alt+C` to toggle the overlay
   - Type your message and hit `Enter` or click `Translate` for outgoing translations
   - Use the language dropdown to select your target language

## Configuration

The application comes with sensible defaults, but you can modify:
- Default languages
- Hotkey combinations
- UI appearance
- OCR settings

Configuration files are located in the `src/config` directory.

## Troubleshooting

1. **OCR not working:**
   - Verify Tesseract is installed correctly
   - Check if language packs are installed
   - Ensure path to Tesseract is correct in settings

2. **Screen capture issues:**
   - Run the application with administrator privileges
   - Check if screen recording permissions are enabled (Mac)
   - Verify the selected area is visible

3. **Translation not working:**
   - Check internet connection
   - Verify language selection
   - Try selecting a clearer area of text

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Tesseract OCR
- Deep Translator
- MSS for screen capture
- All other open-source contributors