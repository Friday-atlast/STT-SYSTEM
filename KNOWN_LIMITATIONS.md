KNOWN LIMITATIONS — v1.0.0

1) Model binaries not included
- Reason: model files are large and should be downloaded by users. Place a `ggml-*.bin` file in `engine/models/`.

2) Memory and performance
- Small models recommended for Raspberry Pi. Large models may not run on low-RAM devices.

3) No GUI
- The CLI and minimal API are present. A full web UI is planned for future releases.

4) Streaming/real-time
- v1 supports short-duration mic recordings and file transcription. Low-latency streaming is experimental.

5) Cross-platform builds for whisper.cpp
- Building the engine on Windows and ARM may require extra platform steps (see `docs/installation.md`).

Stability statement:
- `Core CLI workflows`: Stable and tested on desktop and Raspberry Pi (tiny/base models).
- `API`: Basic and usable for local deployments; not hardened for public hosting.
- `Experimental`: Streaming, large-model performance tuning, and TTS glue code.
