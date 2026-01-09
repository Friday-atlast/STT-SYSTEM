Final Directory Structure (frozen for v1.0.0)

Root layout (what to expect):

- `api/` — minimal FastAPI routes (optional small API server)
- `audio/` — recording and preprocessing helpers (PyAudio wrapper)
- `cli/` — command-line entrypoint and CLI helpers (`stt_cli.py`)
- `config/` — `config.json` and loader utilities (defaults + version)
- `docs/` — user-facing documentation and guides
- `engine/` — whisper.cpp engine source and `models/` (model binaries not committed)
- `language/` — language resolution and validation helpers
- `output/` — transcripts and generated outputs
- `sample/` — example audio and test samples
- `stt/` — orchestration layer that calls whisper CLI
- `temp_uploads/` — temporary uploads (removed/ignored in v1)
- `VERSION` — current version string (`v1.0.0`)
- `RELEASE_NOTES_v1.0.0.md` — human-friendly release notes
- `ROADMAP.md` — public roadmap for next iterations

Notes:
- Large model binaries must be placed in `engine/models/` by the user.
- `engine/build/` and other build artifacts are ignored in v1 and not part of the release.

This file defines the canonical layout for v1.0.0. Keep changes to the structure deliberate and documented.