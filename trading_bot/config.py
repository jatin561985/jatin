import json
from typing import Dict, Any

def load_config(config_path: str = "config.json") -> Dict[str, Any]:
    """
    Loads the configuration file.
    """
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Error: Configuration file not found at {config_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {config_path}")
        return {}

# Load the configuration once when the module is imported
CONFIG = load_config()

if __name__ == '__main__':
    # For testing purposes, print some values
    if CONFIG:
        print("Configuration loaded successfully.")
        print(f"Bot Name: {CONFIG.get('bot_configuration', {}).get('name')}")
        print(f"Risk per trade: {CONFIG.get('risk_management', {}).get('max_risk_per_trade')}")
    else:
        print("Failed to load configuration.")
