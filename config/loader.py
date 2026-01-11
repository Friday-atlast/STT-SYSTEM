import json
import os

# --- DEFAULTS (Safety Net) ---
# Agar config file gayab ho jaye ya galat ho, toh ye use hoga
DEFAULT_CONFIG = {
    "model_type": "tiny",
    "language": "auto",
    "mic_duration": 5,
    "threads": 4
}

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

def load_config():
    """
    Config load karta hai.
    Priority: config.json > DEFAULT_CONFIG
    """
    config = DEFAULT_CONFIG.copy()
    
    if not os.path.exists(CONFIG_PATH):
        print(f"⚠️  Config file not found at {CONFIG_PATH}. Using defaults.")
        return config
    
    try:
        with open(CONFIG_PATH, 'r') as f:
            user_config = json.load(f)
            # Validate each key
            for key, value in user_config.items():
                if key not in config:
                    print(f"⚠️  Ignoring unknown key: {key}")
                    continue
                
                # Type validation and allowed values
                if key == "model_type" and value not in ["tiny", "base", "small"]:
                    print(f"⚠️  Invalid model_type '{value}'. Using default.")
                    continue
                    
                if key == "mic_duration" and (not isinstance(value, int) or value < 1 or value > 60):
                    print(f"⚠️  mic_duration should be 1-60. Using default.")
                    continue
                    
                if key == "threads" and (not isinstance(value, int) or value < 1 or value > 16):
                    print(f"⚠️  threads should be 1-16. Using default.")
                    continue
                
                config[key] = value
                    
    except json.JSONDecodeError:
        print("❌ config.json is invalid JSON. Using defaults.")
        
    return config