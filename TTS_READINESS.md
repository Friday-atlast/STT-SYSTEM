TTS Integration Readiness — v1.0.0

Short summary (child-friendly):
The system can speak back later — we just need to add the speaker parts.

Why the system is ready:
- Core audio I/O exists (`audio/`) and text output is structured (`output/transcripts/`).
- Orchestration layer (`stt/`) produces clean transcript files that TTS can consume.

What to add for TTS integration:
1) Choose a TTS engine (e.g., Coqui TTS, pyttsx3, or platform-native engines).
2) Add a small adapter module `tts/adapter.py` that accepts transcript filepath or text and outputs audio.
3) Add CLI flag `--speak` to `stt_cli.py` to play transcripts after transcription.
4) Update `docs/usage.md` with TTS instructions and examples.

Performance and packaging notes:
- For offline TTS on Raspberry Pi, prefer lightweight engines or pre-synthesized snippets.
- Bundle TTS as optional dependency to avoid inflating `requirements.txt` for v1.
