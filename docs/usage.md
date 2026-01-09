# Usage — CLI examples and what to expect

This page shows the exact commands you will run and what the system prints and saves.

1) CLI basics
- The CLI is `cli/stt_cli.py`.
- Flags:
  - `--mic` : record from microphone (uses `mic_duration` from `config/config.json`).
  - `--file PATH` : transcribe an audio file.
  - `--lang CODE` : override language (e.g., `en`, `hi`, `auto`).

Examples:

- Live mic (record for default duration from `config`):
```bash
python cli/stt_cli.py --mic
```

- Transcribe a file, auto language:
```bash
python cli/stt_cli.py --file my_audio.wav
```

- Force Hindi transcription:
```bash
python cli/stt_cli.py --file speech.wav --lang hi
```

2) Mic workflow (what happens)
- The CLI records to a temporary WAV file in the project root.
- The tool calls the offline STT engine and saves a transcript in `output/transcripts/`.
- After processing the temp file is deleted.

3) File workflow
- The tool checks that the file exists and then runs transcription.
- Output files are placed in `output/transcripts/` with a timestamped name.

4) Output locations and formats
- Text transcripts: `output/transcripts/{originalname}_{timestamp}.txt`
- JSON metadata (if produced): `output/transcripts/{originalname}_{timestamp}.json`

5) API (brief)
- There is a minimal FastAPI server under `api/`. It is not the primary path for beginners. See `api/server.py` if you want to experiment.
