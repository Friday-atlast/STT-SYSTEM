import os
import time
import sys

# Import our modules
# Path hack to make imports work from root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from audio.mic import record_audio
from stt.offline import transcribe_audio

# --- CONFIG ---
TEMP_AUDIO_FILE = "temp_recording.wav"
RECORD_DURATION = 5  # Seconds to record
LANGUAGE = "auto"    # 'hi' for Hindi, 'en' for English

def main():
    print("=== Offline STT System (v1) ===")
    
    # 1. Start Recording
    # Hum temp file root folder mein hi banayenge
    audio_path = os.path.join(os.getcwd(), TEMP_AUDIO_FILE)
    
    start_time = time.time() # Latency measure start
    
    success = record_audio(audio_path, duration=RECORD_DURATION)
    
    if not success:
        print("❌ Recording failed. Exiting.")
        return

    # 2. Transcribe
    # Note: transcribe_audio ab print bhi karta hai aur file bhi save karta hai
    print(f"\n🧠 Sending to Engine...")
    transcribe_audio(audio_path, language=LANGUAGE)
    
    end_time = time.time() # Latency measure end
    
    # 3. Cleanup (Delete temp file)
    if os.path.exists(audio_path):
        os.remove(audio_path)
        print("🧹 Cleanup: Temp audio deleted.")
        
    # 4. Latency Report
    total_time = end_time - start_time
    # Recording time ko minus karo to asli processing time milega
    processing_time = total_time - RECORD_DURATION
    
    print(f"\n⏱️  Stats:")
    print(f"   Recording: {RECORD_DURATION}s")
    print(f"   Processing: {processing_time:.2f}s")
    print(f"   Total Lag: {processing_time:.2f}s (User wait time)")

if __name__ == "__main__":
    main()