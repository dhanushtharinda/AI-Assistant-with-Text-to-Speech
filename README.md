# AI Assistant with Text-to-Speech 🤖🔊

A feature-rich desktop application that converts text to speech using multiple TTS engines. This AI Assistant provides both offline and online text-to-speech capabilities with an intuitive graphical user interface built with Tkinter.

## Features

- **Multiple TTS Engines**: Choose between offline (pyttsx3) and online (Google TTS) engines
- **Customizable Voice Settings**: 
  - Adjustable speech speed (100-300 WPM)
  - Volume control (0.1-1.0)
- **User-Friendly Interface**: Clean, modern dark-themed GUI
- **Real-time Controls**: Start, stop, and manage speech playback
- **Sample Text Library**: Quick access to sample texts for testing
- **Thread-Safe**: Non-blocking speech synthesis runs in separate threads

## Requirements

- Python 3.7 or higher
- Operating System: Windows, macOS, or Linux

### Dependencies

All required packages are listed in `requirements.txt`:

```
pyttsx3==2.90
gTTS==2.3.2
pygame==2.5.2
requests==2.31.0
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/TEEDEElk/AI-Assistant-with-Text-to-Speech.git
   cd AI-Assistant-with-Text-to-Speech
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python tts_assistant.py
   ```

## Usage

### Basic Usage

1. Launch the application by running `tts_assistant.py`
2. Enter or paste text into the text area
3. Choose your preferred TTS engine:
   - **Offline (pyttsx3)**: Works without internet connection
   - **Google TTS**: Requires internet but provides more natural-sounding voice
4. Adjust speed and volume settings as desired
5. Click "🔊 Speak Text" to hear your text
6. Use "⏹️ Stop" to interrupt playback
7. Click "🗑️ Clear" to reset the text field

### TTS Engines

#### pyttsx3 (Offline)
- Works completely offline
- Uses system's built-in TTS voices
- Adjustable speed and volume
- Instant response

#### Google TTS (gTTS)
- Requires internet connection
- High-quality, natural-sounding voice
- Supports multiple languages (default: English)
- Slight delay for audio generation

### Sample Texts

Three pre-loaded sample texts are available for quick testing:
- Sample 1: Greeting message
- Sample 2: Weather statement
- Sample 3: Technology quote

## Controls

- **Speed Slider**: Control speaking rate from slow (100) to fast (300)
- **Volume Slider**: Adjust output volume from quiet (0.1) to maximum (1.0)
- **Speak Button**: Convert text to speech
- **Stop Button**: Interrupt current speech
- **Clear Button**: Empty the text input field

## Troubleshooting

### Common Issues

**Issue**: "Failed to initialize audio" error
- **Solution**: Ensure your system has audio output capabilities and pygame is properly installed

**Issue**: pyttsx3 not working
- **Solution**: 
  - On Linux: Install espeak with `sudo apt-get install espeak`
  - On macOS: The built-in TTS should work by default
  - On Windows: SAPI5 voices should be available

**Issue**: Google TTS not working
- **Solution**: Check your internet connection and ensure you can reach Google's servers

**Issue**: No sound output
- **Solution**: 
  - Check system volume settings
  - Verify audio drivers are installed
  - Try switching between TTS engines

### Platform-Specific Notes

**Linux**:
- Install espeak for pyttsx3: `sudo apt-get install espeak`
- May need to install additional audio libraries

**macOS**:
- Built-in TTS voices work out of the box
- Ensure microphone/audio permissions are granted

**Windows**:
- SAPI5 voices are used by pyttsx3
- Additional voices can be installed from Windows settings

## File Structure

```
AI-Assistant-with-Text-to-Speech/
├── tts_assistant.py      # Main application file
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── launch.json          # VS Code launch configuration
└── import pyttsx3.txt   # Simple pyttsx3 example
```

## Technical Details

### Architecture

- **GUI Framework**: Tkinter (Python's standard GUI library)
- **Audio Playback**: pygame mixer for gTTS audio files
- **Threading**: Python threading for non-blocking speech synthesis
- **TTS Libraries**: pyttsx3 (offline) and gTTS (online)

### Key Components

1. **TTSAssistant Class**: Main application class managing UI and TTS functionality
2. **setup_ui()**: Creates the graphical interface
3. **speak_with_pyttsx3()**: Handles offline speech synthesis
4. **speak_with_gtts()**: Handles online speech synthesis with audio file management
5. **Threading**: Ensures UI remains responsive during speech playback

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## License

This project is open-source and available for personal and educational use.

## Credits

Built with:
- [pyttsx3](https://github.com/nateshmbhat/pyttsx3) - Python text-to-speech library
- [gTTS](https://github.com/pndurette/gTTS) - Google Text-to-Speech API wrapper
- [pygame](https://www.pygame.org/) - Audio playback library
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - Python GUI framework

## Support

If you encounter any issues or have questions:
1. Check the Troubleshooting section above
2. Review closed issues in the repository
3. Open a new issue with detailed information about your problem

---

**Enjoy using your AI Assistant with Text-to-Speech!** 🎉