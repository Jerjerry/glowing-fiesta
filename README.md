# Story Reader with AI Voice

A simple, easy-to-use text-to-speech application that reads stories using Microsoft Edge's AI voices. Perfect for reading long stories or documents with a natural-sounding voice.

## Features

- 🎯 Simple, clean interface
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

1. Run the program:
```bash
python story_reader.py
```

2. Paste your text into the window
3. Click "Read Story"
4. The program will read your text using AI voice

## Voice Options

The program automatically tries these voices in order:
1. Christopher
2. Guy
3. Eric
4. Davis

If one voice fails, it automatically tries the next one.

## Troubleshooting

If you get connection errors:
1. Check your internet connection
2. Make sure Microsoft Edge is installed
3. Disable VPN if you're using one
4. Check the status message in the app for specific errors

## License

MIT License - Feel free to use and modify as needed.
