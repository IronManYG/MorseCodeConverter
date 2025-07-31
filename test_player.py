"""
Unit tests for the MorseCodePlayer class.

This module contains comprehensive unit tests for the MorseCodePlayer class,
testing both normal operation and edge cases. Since audio playback involves
hardware interaction, some tests use mocking to verify functionality without
actually playing sound.
"""

import unittest
from unittest.mock import patch, MagicMock

import pygame

from morse_code import MorseCodePlayer, AudioError, InputError, AUDIO_CONFIG, MORSE_TIMING


class TestMorseCodePlayer(unittest.TestCase):
    """Test cases for the MorseCodePlayer class."""

    @patch('pygame.mixer.init')
    def setUp(self, mock_mixer_init):
        """Set up test fixtures before each test method."""
        # Mock pygame.mixer.init to avoid actual audio initialization
        self.player = MorseCodePlayer()
        self.mock_mixer_init = mock_mixer_init

        # Sample Morse code strings for testing
        self.morse_samples = [
            "... --- ...",  # SOS
            ".... . .-.. .-.. ---",  # HELLO
            ".- -... -.-.",  # ABC
            ".-.-.- --..-- ..--..",  # .,:
            ".---- ..--- ...--"  # 123
        ]

    def test_init_default_parameters(self):
        """Test initialization with default parameters."""
        # Verify that pygame.mixer.init was called with the correct parameters
        self.mock_mixer_init.assert_called_once_with(
            frequency=AUDIO_CONFIG['sample_rate'],
            size=AUDIO_CONFIG['size'],
            channels=AUDIO_CONFIG['channels']
        )

        # Verify that the player's attributes are set correctly
        self.assertEqual(self.player.frequency, AUDIO_CONFIG['frequency'])

        # Verify timing attributes
        unit_duration = AUDIO_CONFIG['unit_duration']
        self.assertEqual(self.player.dot_length, unit_duration * MORSE_TIMING['dot_length'])
        self.assertEqual(self.player.dash_length, unit_duration * MORSE_TIMING['dash_length'])
        self.assertEqual(self.player.pause, unit_duration * MORSE_TIMING['element_pause'] / 1000)
        self.assertEqual(self.player.char_pause, unit_duration * MORSE_TIMING['character_pause'] / 1000)
        self.assertEqual(self.player.word_pause, unit_duration * MORSE_TIMING['word_pause'] / 1000)

    def test_init_custom_parameters(self):
        """Test initialization with custom parameters."""
        with patch('pygame.mixer.init'):
            custom_frequency = 800
            custom_unit_duration = 150
            player = MorseCodePlayer(frequency=custom_frequency, unit_duration=custom_unit_duration)

            # Verify that the player's attributes are set correctly
            self.assertEqual(player.frequency, custom_frequency)

            # Verify timing attributes
            self.assertEqual(player.dot_length, custom_unit_duration * MORSE_TIMING['dot_length'])
            self.assertEqual(player.dash_length, custom_unit_duration * MORSE_TIMING['dash_length'])
            self.assertEqual(player.pause, custom_unit_duration * MORSE_TIMING['element_pause'] / 1000)
            self.assertEqual(player.char_pause, custom_unit_duration * MORSE_TIMING['character_pause'] / 1000)
            self.assertEqual(player.word_pause, custom_unit_duration * MORSE_TIMING['word_pause'] / 1000)

    def test_init_invalid_parameters(self):
        """Test initialization with invalid parameters."""
        # Test with invalid frequency
        with patch('pygame.mixer.init'), self.assertRaises(TypeError):
            MorseCodePlayer(frequency="not a number")

        # Test with invalid unit_duration
        with patch('pygame.mixer.init'), self.assertRaises(TypeError):
            MorseCodePlayer(unit_duration="not a number")

        # Test with pygame initialization failure
        with patch('pygame.mixer.init', side_effect=pygame.error("Mock error")), self.assertRaises(AudioError):
            MorseCodePlayer()

    @patch('pygame.sndarray.make_sound')
    @patch('pygame.mixer.get_init')
    def test_create_sine_wave(self, mock_get_init, mock_make_sound):
        """Test create_sine_wave method."""
        # Mock pygame.mixer.get_init to return sample rate and channels
        mock_get_init.return_value = (44100, -16, 1)  # sample_rate, size, channels

        # Mock pygame.sndarray.make_sound to return a mock sound object
        mock_sound = MagicMock()
        mock_make_sound.return_value = mock_sound

        # Test with valid duration
        duration = 0.1
        sound = self.player.create_sine_wave(duration)

        # Verify that pygame.mixer.get_init was called
        mock_get_init.assert_called_once()

        # Verify that pygame.sndarray.make_sound was called
        mock_make_sound.assert_called_once()

        # Verify that the returned sound is the mock sound
        self.assertEqual(sound, mock_sound)

        # Test with invalid duration types
        with self.assertRaises(TypeError):
            self.player.create_sine_wave("not a number")

        with self.assertRaises(ValueError):
            self.player.create_sine_wave(0)

        with self.assertRaises(ValueError):
            self.player.create_sine_wave(-1)

        # Test with pygame.mixer not initialized
        mock_get_init.return_value = None
        with self.assertRaises(AudioError):
            self.player.create_sine_wave(duration)

    @patch('time.sleep')
    @patch.object(MorseCodePlayer, 'create_sine_wave')
    def test_play_morse_code(self, mock_create_sine_wave, mock_sleep):
        """Test play_morse_code method."""
        # Mock create_sine_wave to return a mock sound object
        mock_sound = MagicMock()
        mock_create_sine_wave.return_value = mock_sound

        # Test with valid Morse code
        morse_code = "... --- ..."  # SOS
        self.player.play_morse_code(morse_code)

        # Verify that create_sine_wave was called for each dot and dash
        # 3 dots + 3 dashes + 3 dots = 9 calls
        self.assertEqual(mock_create_sine_wave.call_count, 9)

        # Verify that sound.play() was called for each dot and dash
        self.assertEqual(mock_sound.play.call_count, 9)

        # Verify that time.sleep was called for pauses
        # 9 elements + 2 spaces between characters = 11 pauses
        # Plus 1 final word pause = 12 total calls
        self.assertEqual(mock_sleep.call_count, 12)

        # Reset mocks for next test
        mock_create_sine_wave.reset_mock()
        mock_sound.reset_mock()
        mock_sleep.reset_mock()

        # Test with invalid input types
        with self.assertRaises(TypeError):
            self.player.play_morse_code(123)

        with self.assertRaises(InputError):
            self.player.play_morse_code("")

        # Test with invalid characters
        morse_code_with_invalid = "... --- ... !"
        with self.assertRaises(InputError):
            self.player.play_morse_code(morse_code_with_invalid)

    @patch('time.sleep')
    @patch.object(MorseCodePlayer, 'create_sine_wave')
    def test_play_morse_code_timing(self, mock_create_sine_wave, mock_sleep):
        """Test timing in play_morse_code method."""
        # Mock create_sine_wave to return a mock sound object
        mock_sound = MagicMock()
        mock_create_sine_wave.return_value = mock_sound

        # Test with a simple Morse code
        morse_code = ".-"  # A
        self.player.play_morse_code(morse_code)

        # Verify that create_sine_wave was called with correct durations
        # First call should be for dot (dot_length / 1000.0)
        # Second call should be for dash (dash_length / 1000.0)
        mock_create_sine_wave.assert_any_call(self.player.dot_length / 1000.0)
        mock_create_sine_wave.assert_any_call(self.player.dash_length / 1000.0)

        # Verify that time.sleep was called with correct durations
        # Element pause after dot and dash, and word pause at the end
        mock_sleep.assert_any_call(self.player.pause)
        mock_sleep.assert_any_call(self.player.word_pause)

    def test_play_morse_code_exception_handling(self):
        """Test exception handling in play_morse_code method."""
        # Test with an exception during sound creation
        with patch.object(MorseCodePlayer, 'create_sine_wave', side_effect=Exception("Mock error")), self.assertRaises(
                AudioError):
            self.player.play_morse_code("...")


if __name__ == "__main__":
    unittest.main()
