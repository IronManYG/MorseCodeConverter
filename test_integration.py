"""
Integration tests for the Morse Code Converter application.

This module contains integration tests that verify the interaction between
different components of the application, such as the converter, player,
and factory.
"""

import unittest
from unittest.mock import patch

from morse_code import (
    MorseCodeConverterFactory,
    MorseCodePlayer,
    MorseCodeConverter,
    ConfigurationError,
    InputError,
    AudioError
)
from test_fixtures import MorseCodeIntegrationTestCase


class TestMorseCodeIntegration(MorseCodeIntegrationTestCase):
    """Integration tests for the Morse Code Converter application."""

    def test_factory_creates_correct_converter(self):
        """Test that the factory creates the correct converter."""
        # Verify that the converter is an instance of MorseCodeConverter
        self.assertIsInstance(self.converter, MorseCodeConverter)

        # Verify that the converter has the correct Morse code dictionary
        self.assertEqual(self.converter.to_morse_code('SOS'), '... --- ...')

    def test_factory_raises_error_for_invalid_variant(self):
        """Test that the factory raises an error for an invalid variant."""
        with self.assertRaises(ConfigurationError):
            MorseCodeConverterFactory.create_converter('nonexistent_variant')

    def test_register_and_use_new_variant(self):
        """Test registering and using a new Morse code variant."""
        # Create a simple custom Morse code dictionary
        custom_code = {
            'A': '.-',
            'B': '-...',
            'C': '-.-.',
            '1': '.----',
            '2': '..---',
            '3': '...--'
        }

        # Register the new variant
        MorseCodeConverterFactory.register_variant('custom', custom_code)

        # Create a converter using the new variant
        custom_converter = MorseCodeConverterFactory.create_converter('custom')

        # Verify that the converter works with the custom dictionary
        self.assertEqual(custom_converter.to_morse_code('ABC123'), '.- -... -.-. .---- ..--- ...--')

        # Verify that characters not in the dictionary are ignored
        self.assertEqual(custom_converter.to_morse_code('ABCXYZ'), '.- -... -.-.')

    def test_text_to_morse_and_back(self):
        """Test converting text to Morse code and back."""
        original_text = "HELLO WORLD"
        morse_code = self.converter.to_morse_code(original_text)
        converted_text = self.converter.from_morse_code(morse_code)

        # Verify that the text is correctly converted to Morse code and back
        self.assertEqual(converted_text, original_text)

    def test_morse_to_text_and_back(self):
        """Test converting Morse code to text and back."""
        original_morse = ".... . .-.. .-.. ---     .-- --- .-. .-.. -.."
        text = self.converter.from_morse_code(original_morse)
        converted_morse = self.converter.to_morse_code(text)

        # Verify that the Morse code is correctly converted to text and back
        self.assertEqual(converted_morse, original_morse)

    @patch.object(MorseCodePlayer, 'play_morse_code')
    def test_convert_and_play(self, mock_play_morse_code):
        """Test converting text to Morse code and playing it."""
        text = "SOS"
        morse_code = self.converter.to_morse_code(text)

        # Play the Morse code
        self.player.play_morse_code(morse_code)

        # Verify that play_morse_code was called with the correct Morse code
        mock_play_morse_code.assert_called_once_with(morse_code)

    @patch('morse_code.safe_execute')
    def test_safe_execute_with_converter(self, mock_safe_execute):
        """Test using safe_execute with the converter."""
        from morse_code import safe_execute

        # Set up the mock to return a value
        mock_safe_execute.return_value = "... --- ..."

        # Call safe_execute with the converter's to_morse_code method
        result = safe_execute(self.converter.to_morse_code, "SOS")

        # Verify that safe_execute was called with the correct arguments
        mock_safe_execute.assert_called_once()

        # Verify that the result is correct
        self.assertEqual(result, "... --- ...")

    def test_error_handling_integration(self):
        """Test error handling across components."""
        # Test InputError from converter
        with self.assertRaises(InputError):
            self.converter.from_morse_code("")

        # Test AudioError from player (with mocked create_sine_wave)
        with patch.object(MorseCodePlayer, 'create_sine_wave', side_effect=Exception("Mock error")):
            with self.assertRaises(AudioError):
                self.player.play_morse_code("...")


if __name__ == "__main__":
    unittest.main()
