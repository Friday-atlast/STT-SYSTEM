# STT-SYSTEM — Offline Speech-to-Text (Zero-Confusion Guide)

Simple, local speech-to-text for everyone — programmers and non-programmers.

Version: v1.0.0 — Final packaging (see RELEASE_NOTES_v1.0.0.md)

Release notes and roadmap are in the repo root: `RELEASE_NOTES_v1.0.0.md`, `ROADMAP.md`.

This repository contains an offline Speech-to-Text (STT) system built around whisper.cpp with a small Python orchestration layer. The goal: let a first-time user get a working transcription without confusion or guessing.

-----

## What this project does
- Records audio from your microphone and transcribes it locally.
- Transcribes existing audio files (WAV/MP3).
- Runs completely offline (no internet needed).
- Works on low-end machines and Raspberry Pi.

## What this project does NOT do
- Provide a full web UI (there is a minimal API but CLI is primary).
- Send audio or transcripts to the cloud.

-----

## Quick Summary (Copy-paste friendly)

Windows (PowerShell):
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Linux / Raspberry Pi:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then prepare the model (see docs/installation.md): place a `ggml-*.bin` model in `engine/models/` and then run:

```bash
python cli/stt_cli.py --mic
# or
python cli/stt_cli.py --file path/to/audio.wav
```

-----

## Who is this for?
- Beginners who do not know terminals.
- Developers who want a local, private STT tool.
- Hobbyists running on Raspberry Pi or low-power machines.

-----

## System Requirements
- Minimum CPU: Any modern x86 or ARM (Pi 3+/4 recommended for Pi).
- RAM: 2 GB (4 GB recommended for larger models).
- Disk: ~1–2 GB for small models; larger models require more.
- Supported OS: Windows 10/11, Linux (Debian/Ubuntu), Raspberry Pi OS.

Raspberry Pi note: Use `tiny` or `base` models for good performance.

-----

## Files you will use first
- `cli/stt_cli.py` — main command line tool.
- `config/config.json` — safe defaults (model, language, mic_duration).
- `output/transcripts/` — where transcripts are saved.

-----

## More detailed docs
See the `docs/` folder for step-by-step instructions:
- docs/installation.md — Full install + model + build steps
- docs/usage.md — CLI examples, mic and file workflows
- docs/config.md — `config.json` explained (safe defaults)
- docs/faq.md — common errors and fixes
- docs/safety.md — what to avoid changing and beginner safety tips
- docs/directory_structure.md — what each folder does

-----

## Day Summary Checklist
- [ ] Fresh user can run `python cli/stt_cli.py --mic` without help
- [ ] README gives exact commands for Windows and Linux
- [ ] Common install failures covered in docs/installation.md

-----

If you want screenshots, a quick test script, or automated checks, tell me your OS and I will continue.
