"""
Morse Code Converter core package.

This package provides the core functionality for the Morse Code Converter application:
- Converting text to Morse code
- Converting Morse code to text
- Playing Morse code as audio
- Morse code dictionaries for different standards
- User interface functions
- Configuration settings
- Logging system
- Error handling
"""

from .config import AUDIO_CONFIG, MORSE_TIMING, UI_CONFIG, VALIDATION_CONFIG, DEFAULT_MORSE_VARIANT, COLORS
from .converter import MorseCodeConverter
from .errors import (
    MorseCodeError, InputError, ConversionError, AudioError, ConfigurationError,
    handle_error, safe_execute
)
from .factory import MorseCodeConverterFactory
from .logging_config import get_logger, debug, info, warning, error, critical, exception
from .morse_code_data import international_code
from .morse_code_player import MorseCodePlayer
from .ui import (
    get_user_choice, get_yes_or_no, display_menu, display_welcome_message, display_goodbye_message,
    display_section_separator, display_result_header, format_result,
    colorize, colorize_header, colorize_result, colorize_error, colorize_warning
)

__all__ = [
    # Core classes
    'MorseCodeConverter',
    'MorseCodePlayer',
    'international_code',
    'MorseCodeConverterFactory',

    # UI functions
    'get_user_choice',
    'get_yes_or_no',
    'display_menu',
    'display_welcome_message',
    'display_goodbye_message',
    'display_section_separator',
    'display_result_header',
    'format_result',
    'colorize',
    'colorize_header',
    'colorize_result',
    'colorize_error',
    'colorize_warning',

    # Configuration
    'AUDIO_CONFIG',
    'MORSE_TIMING',
    'UI_CONFIG',
    'VALIDATION_CONFIG',
    'DEFAULT_MORSE_VARIANT',
    'COLORS',

    # Logging
    'get_logger',
    'debug',
    'info',
    'warning',
    'error',
    'critical',
    'exception',

    # Error handling
    'MorseCodeError',
    'InputError',
    'ConversionError',
    'AudioError',
    'ConfigurationError',
    'handle_error',
    'safe_execute'
]
