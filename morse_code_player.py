import pygame
import numpy as np
import time


class MorseCodePlayer:
    def __init__(self, frequency=600, unit_duration=100):
        self.frequency = frequency
        self.dot_length = unit_duration
        self.dash_length = unit_duration * 3
        self.pause = unit_duration / 1000
        self.char_pause = unit_duration * 3 / 1000
        self.word_pause = unit_duration * 7 / 1000
        pygame.mixer.init(frequency=44100, size=-16, channels=1)

    def create_sine_wave(self, duration):
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
