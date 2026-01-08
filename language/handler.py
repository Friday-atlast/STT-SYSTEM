# Supported Languages by Whisper (Short list for validation)
SUPPORTED_LANGUAGES = {
    "auto": "Auto Detect",
    "en": "English",
    "hi": "Hindi",
    "mr": "Marathi",
    "ta": "Tamil",
    "te": "Telugu",
    "bn": "Bengali",
    "gu": "Gujarati",
    "kn": "Kannada",
    "ml": "Malayalam",
    "pa": "Punjabi",
    "ur": "Urdu"
}

DEFAULT_LANG = "auto"

def resolve_language(cli_lang=None, config_lang=None):
    """
    Language decide karta hai priority ke base pe:
    1. CLI Argument (Highest Priority)
    2. Config File
    3. Default ('auto')
    """
    
    # 1. Check CLI Argument
    if cli_lang:
        lang = cli_lang.lower().strip()
        if lang in SUPPORTED_LANGUAGES:
            return lang
        else:
            print(f"⚠️  Warning: '{lang}' not supported. Falling back to config.")
    
    # 2. Check Config
    if config_lang:
        lang = config_lang.lower().strip()
        if lang in SUPPORTED_LANGUAGES:
            return lang
            
    # 3. Fallback
    return DEFAULT_LANG

def get_language_name(code):
    return SUPPORTED_LANGUAGES.get(code, "Unknown")