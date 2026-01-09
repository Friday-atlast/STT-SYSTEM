# Directory Structure — What each folder does (simple words)

Root files you will use:
- `README.md` — this quick guide.
- `requirements.txt` — Python packages to install.

Top-level folders:
- `audio/` — code that records audio from your microphone.
- `cli/` — `stt_cli.py` is the command-line tool you use.
- `config/` — `config.json` contains safe defaults the CLI reads.
- `docs/` — this documentation (you are reading it).
- `engine/` — whisper.cpp engine and build files; contains models and compiled binaries.
- `stt/` — orchestration code that calls the engine and writes transcripts.
- `output/transcripts/` — where text output is saved.
- `api/` — optional FastAPI server (advanced use).

How they work together (simple):
1. You run a command in `cli/stt_cli.py`.
2. The CLI uses `config/config.json` to find settings.
3. Audio is recorded (or read from a file) by code in `audio/`.
4. `stt/` calls the whisper engine in `engine/` with the chosen model.
5. Results are written to `output/transcripts/`.
