import os
import subprocess
import sys
import shutil # File move karne ke liye
import json
import time

# Add path to find language module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from language.handler import resolve_language, get_language_name # <--- Import

# Model Mapping Logic
MODEL_MAP = {
    "tiny": "ggml-tiny.bin",
    "base": "ggml-base.bin",
    "small": "ggml-small.bin"
}

def get_model_path(model_type):
    """Model type (tiny/base) se file path nikalta hai"""
    filename = MODEL_MAP.get(model_type, "ggml-tiny.bin") # Default to tiny
    return os.path.join(BASE_DIR, "engine", "models", filename)

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if os.name == 'nt':
    WHISPER_PATH = os.path.join(BASE_DIR, "engine", "whisper.cpp", "build", "bin", "Release", "whisper-cli.exe")
else:
    WHISPER_PATH = os.path.join(BASE_DIR, "engine", "whisper.cpp", "build", "bin", "whisper-cli")

OUTPUT_DIR = os.path.join(BASE_DIR, "output", "transcripts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def transcribe_audio(audio_path, language="auto", model_type="tiny", threads=4):
    """
    Transcribes audio and generates .txt and .json files.
    """
    if not os.path.exists(WHISPER_PATH):
        print(f"❌ Error: Binary missing")
        return
    
    # Dynamic Model Path
    current_model_path = get_model_path(model_type)
    
    if not os.path.exists(current_model_path):
        print(f"❌ Error: Model missing: {current_model_path}")
        return

    # 1. Validate & Resolve Language
    # Note: Yahan hum assume kar rahe hain ki 'language' argument 
    # jo function mein aaya hai, wo final decided language hai.
    # Lekin double safety ke liye hum check kar sakte hain.
    
    final_lang = language
    if final_lang not in ["auto", "en", "hi", "mr", "ta", "te"]: # Simple check
         # Agar complex validation chahiye to handler import karein, 
         # par offline.py engine hai, decision maker nahi.
         # Isliye hum maan ke chalenge ki CLI/Config ne sahi bheja hai.
         pass

    # Log for User
    lang_name = get_language_name(final_lang)
    print(f"🌐 Language Mode: {lang_name} ({final_lang})")

    # File name without extension (e.g. "temp_recording")
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    
    # Hum unique filename banayenge timestamp ke saath taaki purana overwrite na ho
    timestamp = int(time.time())
    unique_name = f"{base_name}_{timestamp}"
    
    # Whisper output file wahin banata hai jahan audio file hoti hai
    # Isliye hum output path logic baad mein handle karenge
    
    print(f"🎤 Processing: {base_name}")

    command = [
        WHISPER_PATH,
        "-m", current_model_path, # <--- Use Dynamic Path
        "-f", audio_path,
        "-l", final_lang,   # <--- Validated Language
        "-t", str(threads),       # <--- Use Configured Threads
        "--no-gpu",
        "-otxt",
        "-oj",
        "-of", os.path.join(OUTPUT_DIR, unique_name)
    ]

    try:
        # Run Whisper
        subprocess.run(command, capture_output=True, text=True, check=True)
        
        # Paths define karo
        txt_path = os.path.join(OUTPUT_DIR, f"{unique_name}.txt")
        json_path = os.path.join(OUTPUT_DIR, f"{unique_name}.json")
        
        print(f"✅ Text Saved: {txt_path}")
        print(f"✅ JSON Saved: {json_path}")

        # Preview Text
        if os.path.exists(txt_path):
            with open(txt_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                print("\n--- Preview ---")
                print(content[:200] + "..." if len(content) > 200 else content)
                print("---------------\n")

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Failed! Code: {e.returncode}")
    except Exception as e:
        print(f"\n❌ Error: {e}")

# --- TEST ---
if __name__ == "__main__":
    if len(sys.argv) > 1:
        transcribe_audio(sys.argv[1])
    else:
        test_audio = os.path.join(BASE_DIR, "engine", "whisper.cpp", "samples", "jfk.wav")
        transcribe_audio(test_audio)