RELEASE NOTES — v1.0.0

Simple explanation (for a 5-year-old):
We finished the toy. It's in a clean box, with a name and instructions. You can play with it now.

What this release includes:
- Core offline STT engine orchestration using `whisper.cpp` (callable via CLI).
- `cli/stt_cli.py` for microphone and file transcription workflows.
- `config/config.json` default settings and `VERSION` file set to `v1.0.0`.
- Full user docs in `docs/` (installation, usage, config, FAQ).
- Small API server scaffolding in `api/` for optional local hosting.
- Output files placed under `output/transcripts/` with timestamped filenames.

What works (tested):
- Local microphone recording → WAV → transcription (tiny/base models).
- File-based transcription for WAV/MP3 samples.
- Runs on low-end hardware including Raspberry Pi (recommend tiny/base models).

What is NOT included in this release:
- Model binaries (place `ggml-*.bin` in `engine/models/`).
- A full-featured web UI (API is present but UI is out of scope for v1).
- Hosted cloud integrations.

Quick troubleshooting pointers:
- If transcription fails, confirm model is present in `engine/models/`.
- Check `config/config.json` for `model_type` and `language`.

Final packaging notes:
- Repo cleaned of transient files and ignored build artifacts.
- `VERSION` set to `v1.0.0` and `config.json` version updated.

Acknowledgements:
- Built around whisper.cpp (see `engine/whisper.cpp/`).
