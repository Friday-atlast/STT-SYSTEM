import argparse
import os
import sys
import time

# --- IMPORT HACK (Taaki root folder ke modules milein) ---
# Hum system ko batate hain ki "ek folder upar (..)" bhi dekho
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Ab hum apne modules import kar sakte hain
from audio.mic import record_audio
from stt.offline import transcribe_audio

def handle_mic(language):
    """Mic se sunta hai aur process karta hai"""
    print("\n🎤 Mode: Live Microphone Input")
    
    # Temp file setup
    temp_file = os.path.join(parent_dir, "temp_cli_recording.wav")
    
    # 1. Record
    start_time = time.time()
    success = record_audio(temp_file, duration=5) # Abhi 5s fixed hai
    
    if not success:
        print("❌ Recording failed.")
        return

    # 2. Transcribe
    print(f"\n🧠 Processing...")
    transcribe_audio(temp_file, language=language)
    
    # 3. Cleanup
    if os.path.exists(temp_file):
        os.remove(temp_file)
        print("🧹 Cleanup: Temp file removed.")
        
    end_time = time.time()
    print(f"⏱️  Total Time: {end_time - start_time:.2f}s")

def handle_file(file_path, language):
    """Existing file ko process karta hai"""
    print(f"\n📁 Mode: File Input")
    
    # Absolute path banao taaki galti na ho
    abs_path = os.path.abspath(file_path)
    
    if not os.path.exists(abs_path):
        print(f"❌ Error: File nahi mili -> {abs_path}")
        return

    print(f"📄 File: {os.path.basename(abs_path)}")
    transcribe_audio(abs_path, language=language)

def main():
    # --- CLI SETUP ---
    parser = argparse.ArgumentParser(
        description="Offline Speech-to-Text Tool (v1.0)",
        epilog="Examples:\n  python cli/stt_cli.py --mic\n  python cli/stt_cli.py --file audio.wav --lang hi",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Arguments define karo
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--mic", action="store_true", help="Record from microphone (5 seconds)")
    group.add_argument("--file", type=str, help="Transcribe an existing audio file")

    parser.add_argument("--lang", type=str, default="auto", help="Language code (e.g., 'en', 'hi'). Default: auto")

    # Arguments parse karo
    args = parser.parse_args()

    print("=== STT CLI Tool ===")

    # Logic route karo
    if args.mic:
        handle_mic(args.lang)
    elif args.file:
        handle_file(args.file, args.lang)

if __name__ == "__main__":
    main()