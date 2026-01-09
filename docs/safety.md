# Beginner Safety Notes

This short guide tells you what is safe to change and what to avoid.

Safe to change:
- `config/config.json` values like `mic_duration`, `model_type`, and `threads`.
- Adding audio files to `sample/` or `temp_uploads/` for testing.

Do NOT change (unless you are a developer):
- `stt/offline.py` internals — this orchestrates the whisper binary.
- `engine/whisper.cpp/*` source files unless you know CMake and build systems.
- Any code under `api/` if you are beginners and only want CLI usage.

Backups:
- Before editing any file you are not comfortable with, make a copy (e.g., `copy config\config.json config\config.json.bak`).

Privacy and safety:
- The system is offline; audio and transcripts stay on your machine in `output/transcripts/`. Delete them if needed.
