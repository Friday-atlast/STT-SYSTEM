import os
import subprocess
import sys
import shutil # File move karne ke liye
import json
import multiprocessing
import time
import platform

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


def get_optimal_threads(config_threads):
    """
    CPU cores check karta hai aur safe limit set karta hai.
    """
    total_cores = multiprocessing.cpu_count()
    
    # User ne jo maanga hai
    requested = int(config_threads)
    
    # Safe limit: Total cores ka 50% - 75% hi use karo
    # Taaki baaki system hang na ho
    safe_limit = max(1, int(total_cores * 0.75))
    
    # Agar user ne zyada maanga hai, toh safe limit pe le aao
    final_threads = min(requested, safe_limit)
    
    # Low-end devices (2 cores) ke liye always 2 ya 1 rakho
    if total_cores <= 2:
        final_threads = max(1, total_cores - 1) # 1 thread chhod do OS ke liye
        
    return str(final_threads)

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_whisper_binary():
    if platform.system() == "Windows":
        return os.path.join(BASE_DIR, "engine", "whisper.cpp", "build", "bin", "Release", "whisper-cli.exe")
    else:  # Linux/Mac/Pi
        return os.path.join(BASE_DIR, "engine", "whisper.cpp", "build", "bin", "whisper-cli")

WHISPER_PATH = get_whisper_binary()

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
    
    # Calculate Smart Threads
    smart_threads = get_optimal_threads(threads)
    print(f"⚙️  Optimized Threads: {smart_threads} (Requested: {threads})")

    print(f"🎤 Processing: {base_name}")

    command = [
        WHISPER_PATH,
        "-m", current_model_path, # <--- Use Dynamic Path
        "-f", audio_path,
        "-l", final_lang,   # <--- Validated Language
        "-t", smart_threads,       # <--- Use Optimized Threads
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

        # Return the path to the saved transcript on success
        return txt_path

    except subprocess.CalledProcessError as e:
        # Print stdout/stderr to help debugging failing Whisper subprocess
        print(f"\n❌ Failed! Code: {e.returncode}")
        try:
            if hasattr(e, 'stdout') and e.stdout:
                print("--- Whisper STDOUT ---")
                print(e.stdout)
            if hasattr(e, 'stderr') and e.stderr:
                print("--- Whisper STDERR ---")
                print(e.stderr)
        except Exception:
            pass
        return None
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None

# --- TEST ---
if __name__ == "__main__":
    if len(sys.argv) > 1:
        transcribe_audio(sys.argv[1])
    else:
        test_audio = os.path.join(BASE_DIR, "engine", "whisper.cpp", "samples", "jfk.wav")
        transcribe_audio(test_audio)