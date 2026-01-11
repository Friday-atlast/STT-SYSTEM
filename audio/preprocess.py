import subprocess
import os

def convert_to_wav_16k(input_path, output_path=None):
	"""
	Audio file ko 16kHz WAV mein convert karta hai (Whisper requirement)
	Requires: ffmpeg installed
	"""
	if output_path is None:
		base = os.path.splitext(input_path)[0]
		output_path = f"{base}_16k.wav"
    
	command = [
		"ffmpeg", "-y",  # Overwrite
		"-i", input_path,
		"-ar", "16000",  # 16kHz sample rate
		"-ac", "1",      # Mono channel
		"-c:a", "pcm_s16le",  # 16-bit PCM
		output_path
	]
    
	try:
		subprocess.run(command, capture_output=True, check=True)
		return output_path
	except subprocess.CalledProcessError as e:
		print(f"❌ FFmpeg conversion failed: {e.stderr}")
		return None
	except FileNotFoundError:
		print("❌ FFmpeg not installed! Install it first.")
		return None


def validate_audio_format(file_path):
	"""
	Check if audio file is valid for whisper
	"""
	valid_extensions = ['.wav', '.mp3', '.m4a', '.flac', '.ogg']
	ext = os.path.splitext(file_path)[1].lower()
    
	if ext not in valid_extensions:
		return False, f"Unsupported format: {ext}"
    
	if not os.path.exists(file_path):
		return False, "File not found"
    
	# File size check (too small = probably empty)
	if os.path.getsize(file_path) < 1000:  # Less than 1KB
		return False, "File too small, possibly empty"
    
	return True, "Valid"

