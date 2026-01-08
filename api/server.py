from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Ensure project root is on sys.path so running `python api/server.py` works
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
from api.routes import router


app = FastAPI(
    title="Offline STT API",
    version="1.0",
    description="API layer for Whisper.cpp based Offline STT Engine"
)

# Routes Jodo
app.include_router(router)

# Static files setup
static_dir = os.path.join(current_dir, "static")
if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def serve_ui():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "STT API is running. Use POST /stt to transcribe."}

if __name__ == "__main__":
    import uvicorn
    # Host 0.0.0.0 matlab local network pe koi bhi access kar sake
    uvicorn.run(app, host="0.0.0.0", port=8000)