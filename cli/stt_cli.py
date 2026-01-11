import argparse
import os
import sys
import time

# Path Setup
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from audio.mic import record_audio
from stt.offline import transcribe_audio
from config.loader import load_config  # <--- Import Loader
from language.handler import resolve_language
from audio.preprocess import validate_audio_format, convert_to_wav_16k

def handle_mic(config, cli_lang=None):
    # Resolve final language using handler (CLI > Config)
    final_lang = resolve_language(cli_lang, config.get('language'))
    duration = config['mic_duration']
    model = config['model_type']
    threads = config['threads']

    print(f"\n🎤 Mode: Live Mic | Model: {model} | Lang: {final_lang} | Threads: {threads}")
    print(f"⏱️  Recording Duration: {duration}s (Change in config.json)")
    
    temp_file = os.path.join(parent_dir, "temp_cli_recording.wav")
    
    # Pass duration from config
    success = record_audio(temp_file, duration=duration)
    
    if not success:
        print("❌ Recording failed.")
        return

    print(f"\n🧠 Processing...")
    # Validate recorded file
    ok, msg = validate_audio_format(temp_file)
    if not ok:
        print(f"❌ Audio validation failed: {msg}")
        if msg.startswith("Unsupported format"):
            converted = convert_to_wav_16k(temp_file)
            if converted:
                temp_to_send = converted
            else:
                return
        else:
            return
    else:
        temp_to_send = temp_file

    transcribe_audio(temp_to_send, language=final_lang, model_type=model, threads=threads)
    
    if os.path.exists(temp_file):
        os.remove(temp_file)

def handle_file(file_path, config, cli_lang=None):
    final_lang = resolve_language(cli_lang, config.get('language'))
    model = config['model_type']
    threads = config['threads']
    
    print(f"\n📁 Mode: File | Model: {model} | Lang: {final_lang}")
    
    abs_path = os.path.abspath(file_path)
    if not os.path.exists(abs_path):
        print(f"❌ Error: File not found -> {abs_path}")
        return

    # Validate input file and convert if needed
    ok, msg = validate_audio_format(abs_path)
    if not ok:
        print(f"❌ Audio validation failed: {msg}")
        return

    ext = os.path.splitext(abs_path)[1].lower()
    converted_path = None
    if ext != '.wav':
        converted_path = convert_to_wav_16k(abs_path)

    try:
        to_transcribe = converted_path if converted_path else abs_path
        transcribe_audio(to_transcribe, language=final_lang, model_type=model, threads=threads)
    finally:
        if converted_path and os.path.exists(converted_path):
            os.remove(converted_path)

def main():
    # 1. Load Config
    config = load_config()

    # --- CLI SETUP (UPDATED HELP) ---
    parser = argparse.ArgumentParser(
        description="""
🎙️  Offline Speech-to-Text Tool (v1.0)
-------------------------------------
A privacy-focused, offline STT engine powered by Whisper.cpp.
Optimized for low-end devices (CPU Only).
        """,
        epilog="""
Examples:
  # 1. Live Mic Recording (Uses config duration)
  python cli/stt_cli.py --mic

  # 2. Transcribe File (Auto Language)
  python cli/stt_cli.py --file my_audio.wav

  # 3. Force Hindi Language
  python cli/stt_cli.py --file speech.wav --lang hi

  # 4. Override Config Defaults
  (Edit config/config.json to change model/duration permanently)
        """,
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Command Group
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--mic", 
        action="store_true", 
        help=f"Record from microphone (Default: {config['mic_duration']}s, Model: {config['model_type']})"
    )
    group.add_argument(
        "--file", 
        type=str, 
        metavar="PATH", 
        help="Transcribe an existing audio file (WAV/MP3)"
    )

    # Optional Arguments
    parser.add_argument(
        "--lang", 
        type=str, 
        metavar="CODE",
        help=f"Language code (e.g., 'en', 'hi', 'auto').\n(Current Config: {config['language']})"
    )

    args = parser.parse_args()

    print("=== STT CLI Tool ===")

    if args.mic:
        handle_mic(config, args.lang)
    elif args.file:
        handle_file(args.file, config, args.lang)

if __name__ == "__main__":
    main()