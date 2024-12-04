# Story Reader with AI Voice

A simple, easy-to-use text-to-speech application that reads stories using Microsoft Edge's AI voices. Perfect for reading stories in both English and Spanish with natural-sounding voices.

## Features

- 🎯 Simple, clean interface
- 🌎 Bilingual support (English and Spanish)
- 🔍 Automatic language detection
- 📖 Handles very long texts (6000+ characters per chunk)
- 🎙️ High-quality Microsoft Edge AI voices
- 🔄 Automatic voice fallback system
- ⚡ Smooth reading between text chunks
- 📱 Clear status updates and error messages

## Requirements

- Windows OS
- Python 3.11+
- Microsoft Edge installed
- Internet connection

## Installation

1. Make sure you have Python 3.11 or newer installed
2. Install the requirements:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the program using the provided batch file:
```bash
read.bat
```
Or directly with Python:
```bash
python story_reader.py
```

2. Paste your text into the window (English or Spanish)
3. Click "Read Story"
4. The program will automatically detect the language and use appropriate voices

## Voice Options

The program automatically selects voices based on the text language:

### Spanish Text
1. Elvira (Spain Spanish - Female)
2. Beatriz (Mexican Spanish - Female)
3. Alvaro (Spain Spanish - Male)
4. Jorge (Mexican Spanish - Male)

### English Text
1. Christopher
2. Guy
3. Eric
4. Davis

If one voice fails, it automatically tries the next one in the list.

## Language Detection

The program automatically detects Spanish text by looking for:
- Spanish-specific characters (á, é, í, ó, ú, ñ, ¿, ¡)
- Common Spanish words and phrases

No manual language selection needed - just paste your text and click Read!

## Troubleshooting

If you get connection errors:
1. Check your internet connection
2. Make sure Microsoft Edge is installed
3. Disable VPN if you're using one
4. Check the status message in the app for specific errors

## License

MIT License - Feel free to use and modify as needed.
