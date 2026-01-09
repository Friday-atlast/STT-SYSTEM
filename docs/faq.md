# FAQ — Common problems and fixes

Q: Audio not recording / mic not working
- Check your microphone is connected and not in use by another app.
- On Windows, ensure the app (PowerShell) has microphone permission: Settings → Privacy → Microphone.
- Run a quick test recorder (Windows Voice Recorder) to verify hardware.

Q: "File not found" when using `--file`
- Make sure you give the correct path.
- Use an absolute path if in doubt: `python cli/stt_cli.py --file C:\path\to\file.wav`.

Q: Transcription is empty or gibberish
- Try a different model (from `tiny` → `base`).
- Ensure the audio is clear and sampled at 16 kHz or higher.

Q: Too slow / Very long processing
- Use a smaller model (`tiny`) or increase `threads` in `config/config.json`.
- On Raspberry Pi, Intel/ARM hardware limits speed; use `tiny`.

Q: Language detected incorrectly
- Force the language with `--lang CODE`, e.g., `--lang hi` for Hindi.

Q: `ModuleNotFoundError` or missing dependency
- Activate the virtual environment and run `pip install -r requirements.txt`.

If you still fail, copy the exact console output and open an issue with the text.
