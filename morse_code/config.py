"""
Configuration module for the Morse Code Converter application.

This module provides configuration settings for the Morse Code Converter application,
including audio parameters, default values, and other application settings.
"""

import sys
from typing import Dict, List, Set, Union, Any

# Import error handling after checking for circular imports
if 'morse_code.errors' in sys.modules:
    from .errors import ConfigurationError
else:
    # Define a simple error class for use during initialization
    class ConfigurationError(Exception):
        """Exception raised for errors in configuration."""
        pass

# Audio configuration
AUDIO_CONFIG: Dict[str, Union[int, float]] = {
    'frequency': 600,  # Hz
    'unit_duration': 100,  # ms
    'sample_rate': 44100,  # Hz
    'channels': 1,  # mono
    'size': -16,  # signed 16-bit
}

# Morse code timing configuration (in units)
MORSE_TIMING: Dict[str, int] = {
    'dot_length': 1,
    'dash_length': 3,
    'element_pause': 1,
    'character_pause': 3,
    'word_pause': 7,
}

# Terminal colors
COLORS: Dict[str, str] = {
    'RESET': '\033[0m',
    'BLACK': '\033[30m',
    'RED': '\033[31m',
    'GREEN': '\033[32m',
    'YELLOW': '\033[33m',
    'BLUE': '\033[34m',
    'MAGENTA': '\033[35m',
    'CYAN': '\033[36m',
    'WHITE': '\033[37m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m',
}

# UI configuration
UI_CONFIG: Dict[str, Union[List[str], str, Dict[str, str]]] = {
    'menu_options': [
        '1. Convert Text to Morse Code and Optionally Play Sound',
        '2. Convert Morse Code to Text and Optionally Play Sound',
        '3. Play Morse Code Sound',
        '4. Exit',
    ],
    'welcome_message': '''
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║       INTERNATIONAL MORSE CODE CONVERTER AND PLAYER          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
''',
    'goodbye_message': '''
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  Thank you for using the Morse Code Converter and Player!    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
''',
    'menu_header': '''
╔══════════════════════════════════════════════════════════════╗
║                         MAIN MENU                            ║
╚══════════════════════════════════════════════════════════════╝
''',
    'section_separator': '──────────────────────────────────────────────────────────',
    'result_header': '''
╔══════════════════════════════════════════════════════════════╗
║                          RESULT                              ║
╚══════════════════════════════════════════════════════════════╝
''',
}

# Validation configuration
VALIDATION_CONFIG: Dict[str, Set[str]] = {
    'valid_morse_chars': {'.', '-', ' '},
    'valid_menu_choices': {'1', '2', '3', '4'},
    'valid_yes_responses': {'y', 'yes'},
    'valid_no_responses': {'n', 'no'},
}

# Default Morse code variant
DEFAULT_MORSE_VARIANT: str = 'international'


def validate_config() -> None:
    """
    Validate the configuration parameters.
    
    This function checks that all required configuration parameters are present
    and have the correct types. It raises a ConfigurationError if any validation fails.
    
    Returns:
        None
        
    Raises:
        ConfigurationError: If any configuration parameter is invalid.
    """
    # Validate AUDIO_CONFIG
    required_audio_params = {
        'frequency': (int, float),
        'unit_duration': (int, float),
        'sample_rate': int,
        'channels': int,
        'size': int
    }
    _validate_config_dict(AUDIO_CONFIG, required_audio_params, 'AUDIO_CONFIG')

    # Additional validation for AUDIO_CONFIG values
    if AUDIO_CONFIG['frequency'] <= 0:
        raise ConfigurationError("AUDIO_CONFIG['frequency'] must be positive")
    if AUDIO_CONFIG['unit_duration'] <= 0:
        raise ConfigurationError("AUDIO_CONFIG['unit_duration'] must be positive")
    if AUDIO_CONFIG['sample_rate'] <= 0:
        raise ConfigurationError("AUDIO_CONFIG['sample_rate'] must be positive")
    if AUDIO_CONFIG['channels'] not in [1, 2]:
        raise ConfigurationError("AUDIO_CONFIG['channels'] must be 1 (mono) or 2 (stereo)")

    # Validate MORSE_TIMING
    required_timing_params = {
        'dot_length': int,
        'dash_length': int,
        'element_pause': int,
        'character_pause': int,
        'word_pause': int
    }
    _validate_config_dict(MORSE_TIMING, required_timing_params, 'MORSE_TIMING')

    # Additional validation for MORSE_TIMING values
    for param, value in MORSE_TIMING.items():
        if value <= 0:
            raise ConfigurationError(f"MORSE_TIMING['{param}'] must be positive")

    # Validate UI_CONFIG
    required_ui_params = {
        'menu_options': list,
        'welcome_message': str,
        'goodbye_message': str
    }
    _validate_config_dict(UI_CONFIG, required_ui_params, 'UI_CONFIG')

    # Additional validation for UI_CONFIG values
    if len(UI_CONFIG['menu_options']) == 0:
        raise ConfigurationError("UI_CONFIG['menu_options'] must not be empty")

    # Validate VALIDATION_CONFIG
    required_validation_params = {
        'valid_morse_chars': set,
        'valid_menu_choices': set,
        'valid_yes_responses': set,
        'valid_no_responses': set
    }
    _validate_config_dict(VALIDATION_CONFIG, required_validation_params, 'VALIDATION_CONFIG')

    # Additional validation for VALIDATION_CONFIG values
    if len(VALIDATION_CONFIG['valid_morse_chars']) == 0:
        raise ConfigurationError("VALIDATION_CONFIG['valid_morse_chars'] must not be empty")
    if len(VALIDATION_CONFIG['valid_menu_choices']) == 0:
        raise ConfigurationError("VALIDATION_CONFIG['valid_menu_choices'] must not be empty")
    if len(VALIDATION_CONFIG['valid_yes_responses']) == 0:
        raise ConfigurationError("VALIDATION_CONFIG['valid_yes_responses'] must not be empty")
    if len(VALIDATION_CONFIG['valid_no_responses']) == 0:
        raise ConfigurationError("VALIDATION_CONFIG['valid_no_responses'] must not be empty")

    # Validate DEFAULT_MORSE_VARIANT
    if not isinstance(DEFAULT_MORSE_VARIANT, str):
        raise ConfigurationError("DEFAULT_MORSE_VARIANT must be a string")
    if DEFAULT_MORSE_VARIANT == '':
        raise ConfigurationError("DEFAULT_MORSE_VARIANT must not be empty")


def _validate_config_dict(config_dict: Dict[str, Any], required_params: Dict[str, Any], dict_name: str) -> None:
    """
    Validate a configuration dictionary against required parameters.
    
    Args:
        config_dict: The configuration dictionary to validate.
        required_params: A dictionary mapping parameter names to their expected types.
        dict_name: The name of the configuration dictionary (for error messages).
        
    Raises:
        ConfigurationError: If any required parameter is missing or has the wrong type.
    """
    for param, expected_type in required_params.items():
        if param not in config_dict:
            raise ConfigurationError(f"Missing required parameter '{param}' in {dict_name}")

        if isinstance(expected_type, tuple):
            if not isinstance(config_dict[param], expected_type):
                type_names = ' or '.join(t.__name__ for t in expected_type)
                raise ConfigurationError(
                    f"{dict_name}['{param}'] must be of type {type_names}, got {type(config_dict[param]).__name__}"
                )
        elif not isinstance(config_dict[param], expected_type):
            raise ConfigurationError(
                f"{dict_name}['{param}'] must be of type {expected_type.__name__}, got {type(config_dict[param]).__name__}"
            )


# Validate configuration when the module is loaded
try:
    validate_config()
except ConfigurationError as e:
    print(f"Configuration error: {str(e)}")
    print("The application may not function correctly.")
    # Don't exit here, as this would prevent the application from starting
    # Just log the error and continue
