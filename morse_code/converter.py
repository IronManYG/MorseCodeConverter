"""
Module for converting between text and Morse code.

This module provides the MorseCodeConverter class for converting text to Morse code
and vice versa using a provided Morse code dictionary.
"""

from typing import Dict, List, Set

from .errors import InputError
from .logging_config import get_logger

# Create a logger for this module
logger = get_logger(__name__)


class MorseCodeConverter:
    """
    A class for converting between text and Morse code.
    
    This class provides methods to convert text to Morse code and vice versa
    using a provided Morse code dictionary.
    """

    def __init__(self, morse_code_dict: Dict[str, str]) -> None:
        """
        Initialize the MorseCodeConverter with a Morse code dictionary.
        
        Args:
            morse_code_dict (Dict[str, str]): A dictionary mapping characters to their Morse code representations.
            
        Raises:
            TypeError: If morse_code_dict is not a dictionary.
        """
        if not isinstance(morse_code_dict, dict):
            raise TypeError("morse_code_dict must be a dictionary")
        self.morse_code_dict: Dict[str, str] = morse_code_dict
        logger.debug(f"Initialized MorseCodeConverter with dictionary containing {len(morse_code_dict)} characters")

    def to_morse_code(self, input_string: str) -> str:
        """
        Converts a string to Morse code, ignoring characters not in the Morse code dictionary.

        Args:
            input_string (str): The string to convert.

        Returns:
            str: The converted Morse code string.
            
        Raises:
            TypeError: If input_string is not a string.
            InputError: If input_string is empty.
        """
        # Validate input
        if not isinstance(input_string, str):
            raise TypeError("input_string must be a string")

        if not input_string:
            raise InputError("input_string cannot be empty")

        upper_string = input_string.upper()
        morse_code_list: List[str] = []
        invalid_chars: List[str] = []

        for char in upper_string:
            if char in self.morse_code_dict:
                morse_code_list.append(self.morse_code_dict[char])
            elif char == ' ':
                morse_code_list.append('   ')  # Three spaces to separate words in Morse code
            else:
                invalid_chars.append(char)

        # Report invalid characters at the end instead of logging for each one
        if invalid_chars:
            unique_invalid: Set[str] = set(invalid_chars)
            logger.warning(
                f"The following characters are not valid Morse code characters and will be ignored: {', '.join(unique_invalid)}")

        return ' '.join(morse_code_list)

    def from_morse_code(self, morse_string: str) -> str:
        """
        Converts a Morse code string to text.
        
        This method takes a Morse code string and converts it back to text using
        the Morse code dictionary provided during initialization. Characters not
        found in the dictionary are ignored.
        
        Args:
            morse_string (str): The Morse code string to convert.
                                Words should be separated by three spaces.
                                Characters within a word should be separated by a single space.
        
        Returns:
            str: The decoded text message.
            
        Raises:
            TypeError: If morse_string is not a string.
            InputError: If morse_string is empty or contains invalid Morse code characters.
        """
        # Validate input
        if not isinstance(morse_string, str):
            raise TypeError("morse_string must be a string")

        if not morse_string:
            raise InputError("morse_string cannot be empty")

        # Check if the string contains only valid Morse code characters (., -, space)
        valid_chars: Set[str] = {'.', '-', ' '}
        invalid_chars: List[str] = [char for char in morse_string if char not in valid_chars]
        if invalid_chars:
            unique_invalid: Set[str] = set(invalid_chars)
            raise InputError(
                f"morse_string contains invalid characters: {', '.join(unique_invalid)}. "
                f"Only dots (.), dashes (-), and spaces are allowed."
            )

        # Invert the Morse code dictionary to map Morse codes to characters
        # This creates a new dictionary where the keys are Morse codes and the values are characters
        # For example, {'A': '.-'} becomes {'.-': 'A'}
        # This allows us to look up a Morse code and find the corresponding character
        text_dict: Dict[str, str] = {v: k for k, v in self.morse_code_dict.items()}

        # Split the Morse code string into words using three spaces as the delimiter
        # In Morse code, words are separated by three spaces
        # For example, ".... . .-.. .-.. ---   .-- --- .-. .-.. -.." represents "HELLO WORLD"
        morse_words: List[str] = morse_string.split('   ')  # Three spaces to separate words
        decoded_message: List[str] = []  # Will hold the decoded words
        invalid_codes: List[str] = []  # Will track any invalid Morse codes encountered

        # Process each word in the Morse code string
        for word in morse_words:
            decoded_chars: List[str] = []  # Will hold the decoded characters for this word

            # Split the word into individual Morse code characters
            # In Morse code, characters within a word are separated by a single space
            for char in word.split():
                if char in text_dict:
                    # If the Morse code is valid, look up the corresponding character
                    decoded_chars.append(text_dict[char])
                else:
                    # If the Morse code is not valid, track it for later reporting
                    invalid_codes.append(char)

            # Join the decoded characters to form a word and add it to the decoded message
            decoded_message.append(''.join(decoded_chars))

        # Report invalid Morse codes
        if invalid_codes:
            unique_invalid: Set[str] = set(invalid_codes)
            logger.warning(f"The following Morse codes are not valid and will be ignored: {', '.join(unique_invalid)}")

        return ' '.join(decoded_message)
