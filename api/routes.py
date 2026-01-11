from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
import sys
import subprocess
import traceback

# Import our existing logic
# (Path setup taaki root se import ho sake)
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from stt.offline import transcribe_audio
from config.loader import load_config

router = APIRouter()
config = load_config()

# Temp storage for uploads
UPLOAD_DIR = os.path.join(root_dir, "temp_uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/stt")
async def speech_to_text(file: UploadFile = File(...), lang: str = "auto"):
    """
    Endpoint: Audio file leta hai -> Text return karta hai.
    """
    # 1. Validation (Kya ye audio file hai?)
    if not file.filename.endswith(('.wav', '.mp3', '.m4a')):
        raise HTTPException(status_code=400, detail="Only audio files (.wav, .mp3, .m4a) allowed")

    # 2. Save Uploaded File Temporarily
    temp_path = os.path.join(UPLOAD_DIR, f"api_{file.filename}")
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        print(f"📥 API received file: {temp_path}")

        # 3. Call STT Engine (now returns the transcript .txt path or None)
        output_txt_path = transcribe_audio(
            temp_path,
            language=lang,
            model_type=config['model_type'],
            threads=config['threads']
        )

        if not output_txt_path or not os.path.exists(output_txt_path):
            raise HTTPException(status_code=500, detail="Transcription failed inside engine")

        # Read the text content
        with open(output_txt_path, "r", encoding="utf-8") as f:
            transcribed_text = f.read().strip()

        return {
            "status": "success",
            "language": lang,
            "text": transcribed_text
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"File not found: {str(e)}")

    except PermissionError as e:
        raise HTTPException(status_code=403, detail=f"Permission denied: {str(e)}")

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Whisper engine failed: {e.stderr}")

    except Exception as e:
        # Log full traceback for debugging
        print(f"❌ Unexpected error:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")

    finally:
        # Cleanup upload
        if os.path.exists(temp_path):
            os.remove(temp_path)