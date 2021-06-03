from typing import Dict

DEFAULTS = {"output_path": "safetab_tables", "limit": 5}


def load_config(config) -> Dict:
    """
    Takes in safetab configuration and changes these key-value pairs
    where indicated by the safetab config. All other key-value pairs
    are left as default values

    Args:
        config (dict): dictionary of the safetab configuration
            taken from json

    Returns:
        Dict (cfg): Configuration dictionary to be passed to entry point.
    """
    cfg = DEFAULTS.copy()
    cfg.update(config)
    return cfg
