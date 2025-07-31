"""
Test fixtures and test data for the Morse Code Converter project.

This module provides common test fixtures and test data that can be used
by all test files in the project, promoting code reuse and consistency.
"""

import unittest
from unittest.mock import patch, MagicMock

from morse_code import (
    MorseCodeConverter,
    MorseCodePlayer,
    MorseCodeConverterFactory,
    international_code,
    AUDIO_CONFIG,
    MORSE_TIMING
)

# Common test data
TEXT_TO_MORSE = {
    "HELLO": ".... . .-.. .-.. ---",
    "WORLD": ".-- --- .-. .-.. -..",
    "SOS": "... --- ...",
    "1234": ".---- ..--- ...-- ....-",
    "HELLO WORLD": ".... . .-.. .-.. ---     .-- --- .-. .-.. -..",
    "!?.": "-.-.-- ..--.. .-.-.-",
    "ABC": ".- -... -.-."
}

MORSE_TO_TEXT = {morse: text for text, morse in TEXT_TO_MORSE.items()}

# Additional Morse code samples for testing
MORSE_SAMPLES = [
    "... --- ...",  # SOS
    ".... . .-.. .-.. ---",  # HELLO
    ".- -... -.-.",  # ABC
    ".-.-.- --..-- ..--..",  # .,:
    ".---- ..--- ...--"  # 123
]

# Custom Morse code dictionary for testing variant registration
CUSTOM_CODE = {
    'A': '.-',
    'B': '-...',
    'C': '-.-.',
    '1': '.----',
    '2': '..---',
    '3': '...--'
}


class MorseCodeConverterTestCase(unittest.TestCase):
    """Base test case for MorseCodeConverter tests."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.converter = MorseCodeConverter(international_code)
        self.text_samples = TEXT_TO_MORSE
        self.morse_samples = MORSE_TO_TEXT


class MorseCodePlayerTestCase(unittest.TestCase):
    """Base test case for MorseCodePlayer tests."""

    @patch('pygame.mixer.init')
    def setUp(self, mock_mixer_init):
        """Set up test fixtures before each test method."""
        # Mock pygame.mixer.init to avoid actual audio initialization
        self.player = MorseCodePlayer()
        self.mock_mixer_init = mock_mixer_init
        self.morse_samples = MORSE_SAMPLES

    def verify_player_attributes(self, player, frequency=None, unit_duration=None):
        """Verify that the player's attributes are set correctly."""
        frequency = frequency if frequency is not None else AUDIO_CONFIG['frequency']
        unit_duration = unit_duration if unit_duration is not None else AUDIO_CONFIG['unit_duration']

        self.assertEqual(player.frequency, frequency)
        self.assertEqual(player.dot_length, unit_duration * MORSE_TIMING['dot_length'])
        self.assertEqual(player.dash_length, unit_duration * MORSE_TIMING['dash_length'])
        self.assertEqual(player.pause, unit_duration * MORSE_TIMING['element_pause'] / 1000)
        self.assertEqual(player.char_pause, unit_duration * MORSE_TIMING['character_pause'] / 1000)
        self.assertEqual(player.word_pause, unit_duration * MORSE_TIMING['word_pause'] / 1000)


class MorseCodeIntegrationTestCase(unittest.TestCase):
    """Base test case for integration tests."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a converter using the factory
        self.converter = MorseCodeConverterFactory.create_converter('international')

        # Create a player with mocked pygame initialization
        with patch('pygame.mixer.init'):
            self.player = MorseCodePlayer()

        self.text_samples = TEXT_TO_MORSE
        self.morse_samples = MORSE_TO_TEXT
        self.custom_code = CUSTOM_CODE


def create_mock_sound():
    """Create a mock sound object for testing."""
    mock_sound = MagicMock()
    return mock_sound


def setup_sine_wave_mocks():
    """Set up mocks for testing the create_sine_wave method."""
    mock_get_init = MagicMock()
    mock_get_init.return_value = (44100, -16, 1)  # sample_rate, size, channels

    mock_make_sound = MagicMock()
    mock_sound = create_mock_sound()
    mock_make_sound.return_value = mock_sound

    return mock_get_init, mock_make_sound, mock_sound
