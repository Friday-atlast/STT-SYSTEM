import pyaudio
import wave
import os

# --- WHISPER SETTINGS ---
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

def record_audio(filename, duration=5):
    """
    Returns: True if success, False if failed
    """
    p = pyaudio.PyAudio()
    
    print(f"\n🎤 Listening... ({duration}s)") # User friendly message
    
    try:
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        frames = []

        for i in range(0, int(RATE / CHUNK * duration)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("🛑 Processing...") # Recording done message
        
        stream.stop_stream()
        stream.close()
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        return True # Signal Success

    except Exception as e:
        print(f"\n❌ Mic Error: {e}")
        return False # Signal Failure
        
    finally:
        p.terminate()

if __name__ == "__main__":
    # Self-test logic
    record_audio("test_mic.wav")