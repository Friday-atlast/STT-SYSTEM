# Configuration — `config/config.json` explained (safe defaults)

Open `config/config.json` in a text editor. Do not change keys you do not understand. Small, safe edits are shown below.

Example `config/config.json` (default):
```json
{
    "model_type": "tiny",
    "language": "auto",
    "mic_duration": 5,
    "threads": 2,
    "ram_mode": "low"
}
```

Fields:
- `model_type`: Which ggml model to use. Safe values: `tiny`, `base`, `small`. Use `tiny` on Raspberry Pi.
- `language`: `auto` => detect automatically. Or use language code like `en`, `hi`.
- `mic_duration`: seconds to record when `--mic` is used (integer).
- `threads`: how many CPU threads to use. Use 1–2 on low-end, more on desktops.
- `ram_mode`: internal optimizations. Leave as `low` unless you know what you're doing.

How to change:
- Edit `config/config.json` with a text editor and save. The CLI reads the file each run.

Safe edits:
- Increase `mic_duration` from 5 to 10 if you want longer recordings.
- Change `model_type` to `base` on a desktop for better accuracy.

Avoid changing the program internals or removing keys.
