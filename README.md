# Story Reader with AI Voice

A simple, elegant text-to-speech application that reads stories using natural-sounding AI voices. Perfect for parents reading stories to children or anyone who wants to listen to text in a natural voice.

## Features

- Clean, intuitive interface
- High-quality AI voices
- Handles long stories smoothly
- Fast and responsive
- Multiple voice fallbacks
- Natural-sounding speech

## Requirements

- Windows OS
- Python 3.11+
- Microsoft Edge (for voice service)
- Internet connection

## Quick Start

1. Install the requirements:
```bash
pip install -r requirements.txt
```

2. Run the program:
```bash
python story_reader.py
```

3. Paste your story and click "Read Story"

## How It Works

The application uses Microsoft Edge's Text-to-Speech service to convert text into natural-sounding speech. It automatically:

- Breaks long text into manageable chunks
- Maintains natural flow between segments
- Handles connection issues gracefully
- Provides clear status updates

## Voice Options

The program uses several high-quality voices:
- Christopher (Primary)
- Guy
- Eric
- Davis

It automatically switches between voices if one is unavailable.

## Troubleshooting

If you encounter connection issues:
1. Check your internet connection
2. Ensure Microsoft Edge is installed
3. Disable VPN if you're using one
4. Check the status messages for specific errors

## License

MIT License - Feel free to use and modify as needed.

## Acknowledgments

- Microsoft Edge TTS for the voice service
- Pygame for audio playback
- Built with Python and Tkinter
