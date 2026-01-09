# Installation — Step-by-step (Zero confusion)

This page shows exact commands and every file you must place. Follow steps exactly. Copy-paste commands for your OS.

1) Prepare Python environment

Windows (PowerShell):
```powershell
cd D:\main\project\Voice\STT-SYSTEM
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Linux / Raspberry Pi:
```bash
cd /home/pi/main/project/Voice/STT-SYSTEM
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2) Models (the engine needs a model file)
- Download a ggml model (small/tiny recommended for Pi). Example model names: `ggml-tiny.en.bin`, `ggml-small.bin`, `ggml-base.bin`.
- Place the model file into `engine/models/`.

Example (Linux):
```bash
mkdir -p engine/models
wget -O engine/models/ggml-tiny.bin https://example.com/path/to/ggml-tiny.bin
```

3) whisper.cpp binary
- If the repo already contains a built binary in `engine/build/bin/`, skip this.
- To build on Windows (Visual Studio / MSVC installed):
  - Open a Developer Command Prompt or use VS tools and run CMake build as documented in the engine/whisper.cpp README.

On Raspberry Pi (armv7/arm64) build steps (summary):
```bash
cd engine/whisper.cpp
mkdir -p build && cd build
cmake ..
cmake --build . -j4
```

If building fails: see the error; common fixes are missing `cmake` or missing `build-essential`/toolchain. Install `cmake` and compilers first.

4) Config defaults
- `config/config.json` contains safe defaults. You can edit `model_type`, `language`, `mic_duration`, `threads`.

5) First run (test)
- Run microphone test:
```bash
python cli/stt_cli.py --mic
```

- Transcribe a file test:
```bash
python cli/stt_cli.py --file sample/example.wav
```

If things fail, see docs/faq.md for exact fixes.
