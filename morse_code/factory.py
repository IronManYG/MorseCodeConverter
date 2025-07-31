"""
Factory module for creating Morse code converters.

This module provides a factory class for creating different types of Morse code converters
based on the specified Morse code variant.
"""

from typing import Dict, List

from .converter import MorseCodeConverter
from .errors import ConfigurationError
from .logging_config import get_logger
from .morse_code_data import international_code

# Create a logger for this module
logger = get_logger(__name__)


class MorseCodeConverterFactory:
    """
    Factory class for creating Morse code converters.
    
    This class provides methods to create instances of MorseCodeConverter
    based on the specified Morse code variant.
    """

    # Dictionary of available Morse code variants
    _variants: Dict[str, Dict[str, str]] = {
        'international': international_code,
        # Add more variants here as they become available
    }

    @classmethod
    def get_available_variants(cls) -> List[str]:
        """
        Get a list of available Morse code variants.
        
        Returns:
            List[str]: A list of available Morse code variant names.
        """
        return list(cls._variants.keys())

    @classmethod
    def create_converter(cls, variant: str = 'international') -> MorseCodeConverter:
        """
        Create a Morse code converter for the specified variant.
        
        Args:
            variant (str): The name of the Morse code variant to use.
                          Default is 'international'.
                          
        Returns:
            MorseCodeConverter: A Morse code converter instance configured for the specified variant.
            
        Raises:
            ConfigurationError: If the specified variant is not available.
        """
        if variant not in cls._variants:
            available_variants = ', '.join(cls.get_available_variants())
            error_msg = f"Morse code variant '{variant}' is not available. Available variants: {available_variants}"
            logger.error(error_msg)
            raise ConfigurationError(error_msg)

        morse_code_dict = cls._variants[variant]
        logger.debug(f"Creating Morse code converter for variant: {variant}")
        return MorseCodeConverter(morse_code_dict)

    @classmethod
    def register_variant(cls, name: str, morse_code_dict: Dict[str, str]) -> None:
        """
        Register a new Morse code variant.
        
        Args:
            name (str): The name of the Morse code variant.
            morse_code_dict (Dict[str, str]): A dictionary mapping characters to their Morse code representations.
            
        Raises:
            TypeError: If morse_code_dict is not a dictionary.
            ValueError: If name is already registered.
        """
        if not isinstance(morse_code_dict, dict):
            raise TypeError("morse_code_dict must be a dictionary")

        if name in cls._variants:
            raise ValueError(f"Morse code variant '{name}' is already registered")

        cls._variants[name] = morse_code_dict
        logger.info(f"Registered new Morse code variant: {name}")
