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
            # Sirf wahi keys update karo jo valid hain
            for key, value in user_config.items():
                if key in config:
                    config[key] = value
                else:
                    print(f"⚠️  Ignoring unknown config key: {key}")
                    
    except json.JSONDecodeError:
        print("❌ Error: config.json is invalid JSON. Using defaults.")
    except Exception as e:
        print(f"❌ Unexpected config error: {e}. Using defaults.")
        
    return config