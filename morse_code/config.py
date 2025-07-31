"""
Configuration module for the Morse Code Converter application.

This module provides configuration settings for the Morse Code Converter application,
including audio parameters, default values, and other application settings.
"""

# Audio configuration
AUDIO_CONFIG = {
    'frequency': 600,  # Hz
    'unit_duration': 100,  # ms
    'sample_rate': 44100,  # Hz
    'channels': 1,  # mono
    'size': -16,  # signed 16-bit
}

# Morse code timing configuration (in units)
MORSE_TIMING = {
    'dot_length': 1,
    'dash_length': 3,
    'element_pause': 1,
    'character_pause': 3,
    'word_pause': 7,
}

# UI configuration
UI_CONFIG = {
    'menu_options': [
        '1. Convert Text to Morse Code and Optionally Play Sound',
        '2. Convert Morse Code to Text and Optionally Play Sound',
        '3. Play Morse Code Sound',
        '4. Exit',
    ],
    'welcome_message': 'Welcome to the International Morse Code Converter and Player',
    'goodbye_message': 'Thank you for using the Morse Code Converter and Player!',
}

# Validation configuration
VALIDATION_CONFIG = {
    'valid_morse_chars': {'.', '-', ' '},
    'valid_menu_choices': {'1', '2', '3', '4'},
    'valid_yes_responses': {'y', 'yes'},
    'valid_no_responses': {'n', 'no'},
}

# Default Morse code variant
DEFAULT_MORSE_VARIANT = 'international'
