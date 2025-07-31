"""
Module for playing Morse code as audio.

This module provides the MorseCodePlayer class for generating and playing
audio representations of Morse code using pygame.
"""

import pygame
import numpy as np
import time
from typing import Optional, Union, Set, List, Dict, Any, Tuple

from .config import AUDIO_CONFIG, MORSE_TIMING
from .errors import AudioError, InputError
from .logging_config import get_logger

# Create a logger for this module
logger = get_logger(__name__)


class MorseCodePlayer:
    """
    A class for playing Morse code as audio.
    
    This class uses pygame to generate and play audio representations of Morse code.
    It follows standard Morse code timing conventions:
    - Dot: 1 unit
    - Dash: 3 units
    - Space between elements: 1 unit
    - Space between characters: 3 units
    - Space between words: 7 units
    """

    def __init__(self, frequency: Optional[Union[int, float]] = None,
                 unit_duration: Optional[Union[int, float]] = None) -> None:
        """
        Initialize the MorseCodePlayer with audio parameters.
        
        Args:
            frequency (int, optional): The frequency of the audio tone in Hz.
                                      If not provided, uses the value from AUDIO_CONFIG.
            unit_duration (int, optional): The duration of one unit in milliseconds.
                                          If not provided, uses the value from AUDIO_CONFIG.
                                          This is used to calculate the duration of dots, dashes, and pauses.
                                          
        Raises:
            AudioError: If pygame initialization fails.
            TypeError: If frequency or unit_duration are not valid numeric types.
        """
        # Validate input parameters
        if frequency is not None and not isinstance(frequency, (int, float)):
            raise TypeError("frequency must be a number")
        if unit_duration is not None and not isinstance(unit_duration, (int, float)):
            raise TypeError("unit_duration must be a number")

        self.frequency: float = frequency if frequency is not None else AUDIO_CONFIG['frequency']
        unit_duration = unit_duration if unit_duration is not None else AUDIO_CONFIG['unit_duration']

        # Set timing based on the unit duration and Morse timing configuration
        self.dot_length: float = unit_duration * MORSE_TIMING['dot_length']
        self.dash_length: float = unit_duration * MORSE_TIMING['dash_length']
        self.pause: float = unit_duration * MORSE_TIMING['element_pause'] / 1000
        self.char_pause: float = unit_duration * MORSE_TIMING['character_pause'] / 1000
        self.word_pause: float = unit_duration * MORSE_TIMING['word_pause'] / 1000

        # Initialize pygame mixer with configuration settings
        try:
            pygame.mixer.init(
                frequency=AUDIO_CONFIG['sample_rate'],
                size=AUDIO_CONFIG['size'],
                channels=AUDIO_CONFIG['channels']
            )
            logger.debug("Pygame mixer initialized successfully")
        except pygame.error as e:
            error_msg = f"Failed to initialize pygame mixer: {str(e)}"
            logger.error(error_msg)
            raise AudioError(error_msg) from e

    def create_sine_wave(self, duration):
        """
        Create a sine wave sound of the specified duration.
        
        This method generates a sine wave at the frequency specified during initialization
        and with the given duration.
        
        Args:
            duration (float): The duration of the sound in seconds.
            
        Returns:
            pygame.mixer.Sound: A pygame Sound object containing the generated sine wave.
            
        Raises:
            TypeError: If duration is not a number.
            AudioError: If there's an error creating the sound.
        """
        # Validate input
        if not isinstance(duration, (int, float)):
            raise TypeError("duration must be a number")

        if duration <= 0:
            raise ValueError("duration must be positive")

        try:
            # Get mixer parameters
            mixer_params = pygame.mixer.get_init()
            if mixer_params is None:
                raise AudioError("Pygame mixer is not initialized")

            sample_rate = mixer_params[0]
            channels = mixer_params[2]
            total_samples = int(duration * sample_rate)

            # Generate sine wave
            wave_samples = (
                    np.sin(2 * np.pi * np.arange(total_samples) * self.frequency / sample_rate) * 32767 * 0.5).astype(
                np.int16)

            if channels == 2:  # For stereo, duplicate the array
                wave_samples = np.repeat(wave_samples.reshape(total_samples, 1), 2, axis=1)

            # Create sound object
            sound = pygame.sndarray.make_sound(wave_samples)
            logger.debug(f"Created sine wave sound of duration {duration} seconds")
            return sound

        except (pygame.error, ValueError, MemoryError) as e:
            error_msg = f"Failed to create sine wave sound: {str(e)}"
            logger.error(error_msg)
            raise AudioError(error_msg) from e

    def play_morse_code(self, morse_string):
        """
        Play a Morse code string as audio.
        
        This method plays the given Morse code string as audio, using dots and dashes
        with appropriate timing according to Morse code standards.
        
        Args:
            morse_string (str): The Morse code string to play.
                               Should contain only dots (.), dashes (-), and spaces.
        
        Note:
            - Dots are played as short beeps (1 unit duration)
            - Dashes are played as long beeps (3 units duration)
            - Spaces between characters are represented by a pause (3 units)
            - Spaces between words are represented by a longer pause (7 units)
            
        Raises:
            TypeError: If morse_string is not a string.
            InputError: If morse_string is empty.
            AudioError: If there's an error during audio playback.
        """
        # Validate input
        if not isinstance(morse_string, str):
            raise TypeError("morse_string must be a string")

        if not morse_string:
            raise InputError("morse_string cannot be empty")

        # Log the Morse code string being played
        logger.debug(f"Playing Morse code: {morse_string}")

        # Check if the string contains only valid Morse code characters
        valid_chars = {'.', '-', ' '}
        invalid_chars = [char for char in morse_string if char not in valid_chars]
        if invalid_chars:
            unique_invalid = set(invalid_chars)
            logger.warning(
                f"The Morse code string contains invalid characters that will be treated as pauses: {', '.join(unique_invalid)}")

        try:
            for char in morse_string:
                if char == '.':
                    sound = self.create_sine_wave(self.dot_length / 1000.0)
                    sound.play()
                    logger.debug("Playing dot")
                elif char == '-':
                    sound = self.create_sine_wave(self.dash_length / 1000.0)
                    sound.play()
                    logger.debug("Playing dash")
                elif char == ' ':
                    time.sleep(self.char_pause)
                    logger.debug("Pausing for character space")
                else:
                    logger.debug(f"Ignoring invalid character: {char}")
                    time.sleep(self.pause)
                time.sleep(self.pause)
            time.sleep(self.word_pause)
            logger.debug("Finished playing Morse code")
        except Exception as e:
            error_msg = f"Error during Morse code playback: {str(e)}"
            logger.error(error_msg)
            raise AudioError(error_msg) from e
