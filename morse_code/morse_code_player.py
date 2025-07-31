"""
Module for playing Morse code as audio.

This module provides the MorseCodePlayer class for generating and playing
audio representations of Morse code using pygame.
"""

import pygame
import numpy as np
import time

from .config import AUDIO_CONFIG, MORSE_TIMING


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

    def __init__(self, frequency=None, unit_duration=None):
        """
        Initialize the MorseCodePlayer with audio parameters.
        
        Args:
            frequency (int, optional): The frequency of the audio tone in Hz.
                                      If not provided, uses the value from AUDIO_CONFIG.
            unit_duration (int, optional): The duration of one unit in milliseconds.
                                          If not provided, uses the value from AUDIO_CONFIG.
                                          This is used to calculate the duration of dots, dashes, and pauses.
        """
        self.frequency = frequency if frequency is not None else AUDIO_CONFIG['frequency']
        unit_duration = unit_duration if unit_duration is not None else AUDIO_CONFIG['unit_duration']

        # Set timing based on the unit duration and Morse timing configuration
        self.dot_length = unit_duration * MORSE_TIMING['dot_length']
        self.dash_length = unit_duration * MORSE_TIMING['dash_length']
        self.pause = unit_duration * MORSE_TIMING['element_pause'] / 1000
        self.char_pause = unit_duration * MORSE_TIMING['character_pause'] / 1000
        self.word_pause = unit_duration * MORSE_TIMING['word_pause'] / 1000

        # Initialize pygame mixer with configuration settings
        pygame.mixer.init(
            frequency=AUDIO_CONFIG['sample_rate'],
            size=AUDIO_CONFIG['size'],
            channels=AUDIO_CONFIG['channels']
        )

    def create_sine_wave(self, duration):
        """
        Create a sine wave sound of the specified duration.
        
        This method generates a sine wave at the frequency specified during initialization
        and with the given duration.
        
        Args:
            duration (float): The duration of the sound in seconds.
            
        Returns:
            pygame.mixer.Sound: A pygame Sound object containing the generated sine wave.
        """
        sample_rate = pygame.mixer.get_init()[0]
        channels = pygame.mixer.get_init()[2]
        total_samples = int(duration * sample_rate)

        wave_samples = (
                np.sin(2 * np.pi * np.arange(total_samples) * self.frequency / sample_rate) * 32767 * 0.5).astype(
            np.int16)

        if channels == 2:  # For stereo, duplicate the array
            wave_samples = np.repeat(wave_samples.reshape(total_samples, 1), 2, axis=1)

        return pygame.sndarray.make_sound(wave_samples)

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
        """
        for char in morse_string:
            if char == '.':
                sound = self.create_sine_wave(self.dot_length / 1000.0)
                sound.play()
            elif char == '-':
                sound = self.create_sine_wave(self.dash_length / 1000.0)
                sound.play()
            elif char == ' ':
                time.sleep(self.char_pause)
            else:
                time.sleep(self.pause)
            time.sleep(self.pause)
        time.sleep(self.word_pause)
