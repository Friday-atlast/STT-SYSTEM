import os
import subprocess
import sys

# --- CONFIGURATION (Paths Setup) ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if os.name == 'nt':
    WHISPER_PATH = os.path.join(BASE_DIR, "engine", "whisper.cpp", "build", "bin", "Release", "whisper-cli.exe")
else:
    WHISPER_PATH = os.path.join(BASE_DIR, "engine", "whisper.cpp", "build", "bin", "whisper-cli")

MODEL_PATH = os.path.join(BASE_DIR, "engine", "models", "ggml-tiny.bin")
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "transcripts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Function ab 'language' parameter bhi leta hai (default 'auto')
def transcribe_audio(audio_path, language="auto"):
    """
    C++ Engine ko call karta hai.
    language: 'en', 'hi', or 'auto'
    """
    
    if not os.path.exists(WHISPER_PATH):
        print(f"❌ Error: Binary missing: {WHISPER_PATH}")
        return
    if not os.path.exists(MODEL_PATH):
        print(f"❌ Error: Model missing: {MODEL_PATH}")
        return
    if not os.path.exists(audio_path):
        print(f"❌ Error: Audio missing: {audio_path}")
        return

    print(f"🎤 Processing: {audio_path}")
    print(f"🌐 Language: {language}")

    # Command Construction
    command = [
        WHISPER_PATH,
        "-m", MODEL_PATH,
        "-f", audio_path,
        "-l", language,    # <--- Language Flag Added
        "--no-gpu"
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        raw_text = result.stdout
        
        filename = os.path.basename(audio_path) + ".txt"
        save_path = os.path.join(OUTPUT_DIR, filename)
        
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(raw_text)

        print(f"✅ Saved to: {save_path}")
        print("\n--- Preview ---")
        # Preview mein non-ascii characters (Hindi) print karne ke liye terminal support chahiye hota hai
        try:
            print(raw_text[:200] + "...")
        except UnicodeEncodeError:
            print("(Preview hidden due to terminal font issues, check file)")
        print("---------------\n")

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Failed! Code: {e.returncode}")

if __name__ == "__main__":
    # Test Logic
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
        
        # User language bhi bata sakta hai argument mein
        # Usage: python offline.py audio.wav hi
        lang = "auto"
        if len(sys.argv) > 2:
            lang = sys.argv[2]
            
        transcribe_audio(audio_file, lang)
    else:
        # Default test
        test_audio = os.path.join(BASE_DIR, "engine", "whisper.cpp", "samples", "jfk.wav")
        transcribe_audio(test_audio, "en")