import os
import subprocess
import sys
import shutil # File move karne ke liye
import json
import time

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if os.name == 'nt':
    WHISPER_PATH = os.path.join(BASE_DIR, "engine", "whisper.cpp", "build", "bin", "Release", "whisper-cli.exe")
else:
    WHISPER_PATH = os.path.join(BASE_DIR, "engine", "whisper.cpp", "build", "bin", "whisper-cli")

MODEL_PATH = os.path.join(BASE_DIR, "engine", "models", "ggml-tiny.bin")
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "transcripts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def transcribe_audio(audio_path, language="auto"):
    """
    Transcribes audio and generates .txt and .json files.
    """
    if not os.path.exists(WHISPER_PATH):
        print(f"❌ Error: Binary missing")
        return
    if not os.path.exists(MODEL_PATH):
        print(f"❌ Error: Model missing")
        return

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
        "-m", MODEL_PATH,
        "-f", audio_path,
        "-l", language,
        "-t", "4",         # 4 Threads for speed
        "--no-gpu",
        "-otxt",           # Output Text file
        "-oj",             # Output JSON file
        "-of", os.path.join(OUTPUT_DIR, unique_name) # Output Filename prefix
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