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

def handle_mic(config, cli_lang=None):
    # Priority: CLI arg > Config > Default
    lang = cli_lang if cli_lang else config['language']
    duration = config['mic_duration']
    model = config['model_type']
    threads = config['threads']

    print(f"\n🎤 Mode: Live Mic | Model: {model} | Lang: {lang} | Threads: {threads}")
    print(f"⏱️  Recording Duration: {duration}s (Change in config.json)")
    
    temp_file = os.path.join(parent_dir, "temp_cli_recording.wav")
    
    # Pass duration from config
    success = record_audio(temp_file, duration=duration)
    
    if not success:
        print("❌ Recording failed.")
        return

    print(f"\n🧠 Processing...")
    transcribe_audio(temp_file, language=lang, model_type=model, threads=threads)
    
    if os.path.exists(temp_file):
        os.remove(temp_file)

def handle_file(file_path, config, cli_lang=None):
    lang = cli_lang if cli_lang else config['language']
    model = config['model_type']
    threads = config['threads']
    
    print(f"\n📁 Mode: File | Model: {model} | Lang: {lang}")
    
    abs_path = os.path.abspath(file_path)
    if not os.path.exists(abs_path):
        print(f"❌ Error: File not found -> {abs_path}")
        return

    transcribe_audio(abs_path, language=lang, model_type=model, threads=threads)

def main():
    # 1. Load Config
    config = load_config()

    parser = argparse.ArgumentParser(description="STT CLI Tool (v1.1)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--mic", action="store_true", help="Record from microphone")
    group.add_argument("--file", type=str, help="Transcribe file")
    
    # Default help mein dikhayenge ki config se kya utha raha hai
    parser.add_argument("--lang", type=str, help=f"Language code (Current Config: {config['language']})")

    args = parser.parse_args()

    print("=== STT CLI Tool ===")

    if args.mic:
        handle_mic(config, args.lang)
    elif args.file:
        handle_file(args.file, config, args.lang)

if __name__ == "__main__":
    main()