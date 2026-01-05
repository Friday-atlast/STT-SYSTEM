# Offline-First STT System

## Overview
A privacy-focused, offline Speech-to-Text engine designed for low-end devices (Raspberry Pi/i3).
Powered by Whisper.cpp and Python.

## Structure
- `engine/`: C++ Core (Whisper)
- `audio/`: Microphone & Audio Processing
- `stt/`: Logic & Orchestration
- `api/`: REST API (FastAPI)

## Setup
1. Create venv: `python -m venv venv`
2. Activate venv.
3. Install reqs: `pip install -r requirements.txt`

## Day 1: Engine Setup
- Whisper.cpp cloned in `engine/`
- Tiny model downloaded.
- Build successful on CPU.