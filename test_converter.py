"""
Unit tests for the MorseCodeConverter class.

This module contains comprehensive unit tests for the MorseCodeConverter class,
testing both normal operation and edge cases.
"""

import unittest

from morse_code import MorseCodeConverter, international_code, InputError
from test_fixtures import MorseCodeConverterTestCase


class TestMorseCodeConverter(MorseCodeConverterTestCase):
    """Test cases for the MorseCodeConverter class."""

    def test_init_valid(self):
        """Test initialization with valid input."""
        converter = MorseCodeConverter(international_code)
        self.assertIsInstance(converter, MorseCodeConverter)
        self.assertEqual(converter.morse_code_dict, international_code)

    def test_init_invalid(self):
        """Test initialization with invalid input."""
        with self.assertRaises(TypeError):
            MorseCodeConverter("not a dictionary")

        with self.assertRaises(TypeError):
            MorseCodeConverter(123)

        with self.assertRaises(TypeError):
            MorseCodeConverter(None)

    def test_to_morse_code_valid(self):
        """Test to_morse_code method with valid input."""
        for text, expected_morse in self.text_samples.items():
            with self.subTest(text=text):
                result = self.converter.to_morse_code(text)
                self.assertEqual(result, expected_morse)

    def test_to_morse_code_case_insensitive(self):
        """Test that to_morse_code is case-insensitive."""
        for text, expected_morse in self.text_samples.items():
            with self.subTest(text=text.lower()):
                result = self.converter.to_morse_code(text.lower())
                self.assertEqual(result, expected_morse)

    def test_to_morse_code_with_invalid_chars(self):
        """Test to_morse_code with characters not in the Morse code dictionary."""
        # Characters not in the dictionary should be ignored with a warning
        result = self.converter.to_morse_code("HELLO@WORLD#123")
        # The @ character is actually in the dictionary as .--.-. and # is ignored
        expected = ".... . .-.. .-.. --- .--.-. .-- --- .-. .-.. -.. .---- ..--- ...--"
        self.assertEqual(result, expected)

    def test_to_morse_code_empty(self):
        """Test to_morse_code with empty input."""
        with self.assertRaises(InputError):
            self.converter.to_morse_code("")

    def test_to_morse_code_non_string(self):
        """Test to_morse_code with non-string input."""
        with self.assertRaises(TypeError):
            self.converter.to_morse_code(123)

        with self.assertRaises(TypeError):
            self.converter.to_morse_code(None)

        with self.assertRaises(TypeError):
            self.converter.to_morse_code(["H", "E", "L", "L", "O"])

    def test_from_morse_code_valid(self):
        """Test from_morse_code method with valid input."""
        for morse, expected_text in self.morse_samples.items():
            with self.subTest(morse=morse):
                result = self.converter.from_morse_code(morse)
                self.assertEqual(result, expected_text)

    def test_from_morse_code_with_invalid_codes(self):
        """Test from_morse_code with Morse codes not in the dictionary."""
        # Invalid Morse codes should be ignored
        with self.assertRaises(InputError):
            self.converter.from_morse_code("... --- ... !!!!")

    def test_from_morse_code_empty(self):
        """Test from_morse_code with empty input."""
        with self.assertRaises(InputError):
            self.converter.from_morse_code("")

    def test_from_morse_code_non_string(self):
        """Test from_morse_code with non-string input."""
        with self.assertRaises(TypeError):
            self.converter.from_morse_code(123)

        with self.assertRaises(TypeError):
            self.converter.from_morse_code(None)

        with self.assertRaises(TypeError):
            self.converter.from_morse_code([".", "-", "."])

    def test_from_morse_code_invalid_chars(self):
        """Test from_morse_code with invalid characters."""
        with self.assertRaises(InputError):
            self.converter.from_morse_code("... --- ... !")

        with self.assertRaises(InputError):
            self.converter.from_morse_code("... --- ... 123")

        with self.assertRaises(InputError):
            self.converter.from_morse_code("... --- ... @#$")

    def test_roundtrip_conversion(self):
        """Test that text can be converted to Morse code and back."""
        for text in self.text_samples.keys():
            with self.subTest(text=text):
                morse = self.converter.to_morse_code(text)
                result = self.converter.from_morse_code(morse)
                self.assertEqual(result, text)

    def test_word_separation(self):
        """Test that words are properly separated in Morse code."""
        text = "HELLO WORLD"
        morse = self.converter.to_morse_code(text)
        # Words should be separated by 5 spaces (3 for word separation + 1 on each side for character separation)
        self.assertIn("---     .--", morse)

        # Convert back and check
        result = self.converter.from_morse_code(morse)
        self.assertEqual(result, text)

    def test_special_characters(self):
        """Test conversion of special characters."""
        text = "!?."
        morse = self.converter.to_morse_code(text)
        self.assertEqual(morse, "-.-.-- ..--.. .-.-.-")

        # Convert back and check
        result = self.converter.from_morse_code(morse)
        self.assertEqual(result, text)

    def test_numbers(self):
        """Test conversion of numbers."""
        text = "1234567890"
        morse = self.converter.to_morse_code(text)
        expected = ".---- ..--- ...-- ....- ..... -.... --... ---.. ----. -----"
        self.assertEqual(morse, expected)

        # Convert back and check
        result = self.converter.from_morse_code(morse)
        self.assertEqual(result, text)


if __name__ == "__main__":
    unittest.main()
