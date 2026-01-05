import pyaudio
import wave
import os

# --- WHISPER OPTIMIZED SETTINGS ---
CHUNK = 1024            # Ek baar mein kitna data padhna hai
FORMAT = pyaudio.paInt16 # 16-bit audio (Standard)
CHANNELS = 1            # Mono audio (Whisper ko Stereo nahi chahiye)
RATE = 16000            # 16kHz (Whisper ka native sample rate)

def record_audio(filename, duration=5):
    """
    Mic se audio record karke WAV file mein save karta hai.
    filename: Path to save file
    duration: Seconds to record
    """
    
    # 1. Setup PyAudio
    p = pyaudio.PyAudio()
    
    print(f"\n🎤 Recording start... ({duration} seconds)")
    print("---------------------------------------")

    try:
        # 2. Open Stream (Mic ON)
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        
        frames = []

        # 3. Recording Loop
        # Rate / Chunk * Duration = Total number of chunks needed
        for i in range(0, int(RATE / CHUNK * duration)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("---------------------------------------")
        print("🛑 Recording finished.")

        # 4. Stop & Close Stream (Mic OFF)
        stream.stop_stream()
        stream.close()
        
        # 5. Save to WAV File
        # Directory ensure karo
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        print(f"✅ Audio saved: {filename}")
        return True

    except Exception as e:
        print(f"\n❌ Error during recording: {e}")
        return False
        
    finally:
        # Hamesha PyAudio terminate karo taaki resource free ho
        p.terminate()

# --- PREPROCESS Placeholder ---
# Day 4 pe hum sirf file bana rahe hain.
def create_placeholder_preprocess():
    preprocess_path = os.path.join(os.path.dirname(__file__), "preprocess.py")
    if not os.path.exists(preprocess_path):
        with open(preprocess_path, "w") as f:
            f.write("# Future home for Noise Reduction logic\n")

# --- TEST RUNNER ---
if __name__ == "__main__":
    # Test recording
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_file = os.path.join(base_dir, "test_mic.wav")
    
    create_placeholder_preprocess()
    
    # 5 second ki recording
    record_audio(test_file, duration=5)