# Morse Code Converter API Documentation

This document provides comprehensive documentation for the Morse Code Converter application's API. It covers all
modules, classes, and functions available for use.

## Table of Contents

1. [Package Overview](#package-overview)
2. [Core Classes](#core-classes)
    - [MorseCodeConverter](#morsecodeconverter)
    - [MorseCodePlayer](#morsecodeplayerclass)
    - [MorseCodeConverterFactory](#morsecodeconverterfactory)
3. [Configuration](#configuration)
    - [Audio Configuration](#audio-configuration)
    - [Morse Timing Configuration](#morse-timing-configuration)
    - [UI Configuration](#ui-configuration)
    - [Validation Configuration](#validation-configuration)
4. [Error Handling](#error-handling)
    - [Exception Classes](#exception-classes)
    - [Error Handling Utilities](#error-handling-utilities)
5. [User Interface](#user-interface)
6. [Logging](#logging)
7. [Morse Code Data](#morse-code-data)
8. [Usage Examples](#usage-examples)

## Package Overview

The Morse Code Converter package (`morse_code`) provides functionality for converting text to Morse code, converting
Morse code to text, and playing Morse code as audio. The package is organized into several modules, each with a specific
responsibility.

```python
from morse_code import (
    MorseCodeConverter,
    MorseCodePlayer,
    MorseCodeConverterFactory,
    international_code
)
```

## Core Classes

### MorseCodeConverter

The `MorseCodeConverter` class is responsible for converting between text and Morse code.

**Module**: `morse_code.converter`

#### Constructor

```python
def __init__(self, morse_code_dict)
```

- **Parameters**:
    - `morse_code_dict` (Dict[str, str]): A dictionary mapping characters to their Morse code representations.
- **Raises**:
    - `TypeError`: If morse_code_dict is not a dictionary.

#### Methods

##### to_morse_code

```python
def to_morse_code(self, input_string: str) -> str
```

Converts a string to Morse code, ignoring characters not in the Morse code dictionary.

- **Parameters**:
    - `input_string` (str): The string to convert.
- **Returns**:
    - str: The converted Morse code string.
- **Raises**:
    - `TypeError`: If input_string is not a string.
    - `InputError`: If input_string is empty.

**Example**:

```python
converter = MorseCodeConverter(international_code)
morse_code = converter.to_morse_code("HELLO")
print(morse_code)  # Output: ".... . .-.. .-.. ---"
```

##### from_morse_code

```python
def from_morse_code(self, morse_string: str) -> str
```

Converts a Morse code string to text.

- **Parameters**:
    - `morse_string` (str): The Morse code string to convert. Words should be separated by three spaces. Characters
      within a word should be separated by a single space.
- **Returns**:
    - str: The decoded text message.
- **Raises**:
    - `TypeError`: If morse_string is not a string.
    - `InputError`: If morse_string is empty or contains invalid Morse code characters.

**Example**:

```python
converter = MorseCodeConverter(international_code)
text = converter.from_morse_code(".... . .-.. .-.. ---")
print(text)  # Output: "HELLO"
```

### MorseCodePlayerClass

The `MorseCodePlayer` class is responsible for playing Morse code as audio.

**Module**: `morse_code.morse_code_player`

#### Constructor

```python
def __init__(self, frequency: Optional[Union[int, float]] = None,
             unit_duration: Optional[Union[int, float]] = None) -> None
```

- **Parameters**:
    - `frequency` (int, optional): The frequency of the audio tone in Hz. If not provided, uses the value from
      AUDIO_CONFIG.
    - `unit_duration` (int, optional): The duration of one unit in milliseconds. If not provided, uses the value from
      AUDIO_CONFIG. This is used to calculate the duration of dots, dashes, and pauses.
- **Raises**:
    - `AudioError`: If pygame initialization fails.
    - `TypeError`: If frequency or unit_duration are not valid numeric types.

#### Methods

##### create_sine_wave

```python
def create_sine_wave(self, duration)
```

Create a sine wave sound of the specified duration.

- **Parameters**:
    - `duration` (float): The duration of the sound in seconds.
- **Returns**:
    - pygame.mixer.Sound: A pygame Sound object containing the generated sine wave.
- **Raises**:
    - `TypeError`: If duration is not a number.
    - `AudioError`: If there's an error creating the sound.

##### play_morse_code

```python
def play_morse_code(self, morse_string)
```

Play a Morse code string as audio.

- **Parameters**:
    - `morse_string` (str): The Morse code string to play. Should contain only dots (.), dashes (-), and spaces.
- **Raises**:
    - `TypeError`: If morse_string is not a string.
    - `InputError`: If morse_string is empty.
    - `AudioError`: If there's an error during audio playback.

**Example**:

```python
player = MorseCodePlayer()
player.play_morse_code(".... . .-.. .-.. ---")  # Plays "HELLO" in Morse code
```

### MorseCodeConverterFactory

The `MorseCodeConverterFactory` class is responsible for creating instances of `MorseCodeConverter` based on the
specified Morse code variant.

**Module**: `morse_code.factory`

#### Class Methods

##### get_available_variants

```python
@classmethod
def get_available_variants(cls) -> List[str]
```

Get a list of available Morse code variants.

- **Returns**:
    - List[str]: A list of available Morse code variant names.

##### create_converter

```python
@classmethod
def create_converter(cls, variant: str = 'international') -> MorseCodeConverter
```

Create a Morse code converter for the specified variant.

- **Parameters**:
    - `variant` (str): The name of the Morse code variant to use. Default is 'international'.
- **Returns**:
    - MorseCodeConverter: A Morse code converter instance configured for the specified variant.
- **Raises**:
    - `ConfigurationError`: If the specified variant is not available.

**Example**:

```python
converter = MorseCodeConverterFactory.create_converter('international')
morse_code = converter.to_morse_code("HELLO")
print(morse_code)  # Output: ".... . .-.. .-.. ---"
```

##### register_variant

```python
@classmethod
def register_variant(cls, name: str, morse_code_dict: Dict[str, str]) -> None
```

Register a new Morse code variant.

- **Parameters**:
    - `name` (str): The name of the Morse code variant.
    - `morse_code_dict` (Dict[str, str]): A dictionary mapping characters to their Morse code representations.
- **Raises**:
    - `TypeError`: If morse_code_dict is not a dictionary.
    - `ValueError`: If name is already registered.

**Example**:

```python
# Create a custom Morse code variant
custom_code = {
    'A': '.-', 'B': '-...', 'C': '-.-.',
    # ... more characters
}

# Register the custom variant
MorseCodeConverterFactory.register_variant('custom', custom_code)

# Create a converter using the custom variant
converter = MorseCodeConverterFactory.create_converter('custom')
```

## Configuration

The Morse Code Converter application uses several configuration dictionaries to control its behavior.

**Module**: `morse_code.config`

### Audio Configuration

The `AUDIO_CONFIG` dictionary contains audio parameters for the `MorseCodePlayer` class.

```python
AUDIO_CONFIG: Dict[str, Union[int, float]] = {
    'frequency': 600,  # Hz
    'unit_duration': 100,  # ms
    'sample_rate': 44100,  # Hz
    'channels': 1,  # mono
    'size': -16,  # signed 16-bit
}
```

### Morse Timing Configuration

The `MORSE_TIMING` dictionary contains timing parameters for Morse code elements.

```python
MORSE_TIMING: Dict[str, int] = {
    'dot_length': 1,
    'dash_length': 3,
    'element_pause': 1,
    'character_pause': 3,
    'word_pause': 7,
}
```

### UI Configuration

The `UI_CONFIG` dictionary contains UI-related settings.

```python
UI_CONFIG: Dict[str, Union[List[str], str]] = {
    'menu_options': [
        '1. Convert Text to Morse Code and Optionally Play Sound',
        '2. Convert Morse Code to Text and Optionally Play Sound',
        '3. Play Morse Code Sound',
        '4. Exit',
    ],
    'welcome_message': 'Welcome to the International Morse Code Converter and Player',
    'goodbye_message': 'Thank you for using the Morse Code Converter and Player!',
}
```

### Validation Configuration

The `VALIDATION_CONFIG` dictionary contains sets of valid characters for validation.

```python
VALIDATION_CONFIG: Dict[str, Set[str]] = {
    'valid_morse_chars': {'.', '-', ' '},
    'valid_menu_choices': {'1', '2', '3', '4'},
    'valid_yes_responses': {'y', 'yes'},
    'valid_no_responses': {'n', 'no'},
}
```

### Default Morse Variant

The `DEFAULT_MORSE_VARIANT` constant specifies the default Morse code variant.

```python
DEFAULT_MORSE_VARIANT: str = 'international'
```

### Configuration Validation

The `validate_config` function validates the configuration parameters.

```python
def validate_config() -> None
```

- **Raises**:
    - `ConfigurationError`: If any configuration parameter is invalid.

## Error Handling

The Morse Code Converter application provides a comprehensive error handling system.

**Module**: `morse_code.errors`

### Exception Classes

#### MorseCodeError

```python
class MorseCodeError(Exception)
```

Base exception class for all Morse Code Converter errors.

#### InputError

```python
class InputError(MorseCodeError)
```

Exception raised for errors in the input.

#### ConversionError

```python
class ConversionError(MorseCodeError)
```

Exception raised for errors during conversion.

#### AudioError

```python
class AudioError(MorseCodeError)
```

Exception raised for errors related to audio playback.

#### ConfigurationError

```python
class ConfigurationError(MorseCodeError)
```

Exception raised for errors in configuration.

### Error Handling Utilities

#### handle_error

```python
def handle_error(error, default_return=None)
```

Handle an error by logging it and returning a default value.

- **Parameters**:
    - `error` (Exception): The error to handle.
    - `default_return`: The value to return if an error occurs. Default is None.
- **Returns**:
    - The default return value.

#### safe_execute

```python
def safe_execute(func, *args, default_return=None, **kwargs)
```

Execute a function safely, handling any exceptions.

- **Parameters**:
    - `func` (callable): The function to execute.
    - `*args`: Positional arguments to pass to the function.
    - `default_return`: The value to return if an error occurs. Default is None.
    - `**kwargs`: Keyword arguments to pass to the function.
- **Returns**:
    - The result of the function call, or the default return value if an error occurs.

**Example**:

```python
result = safe_execute(converter.to_morse_code, "HELLO", default_return="")
if result:
    print(result)
else:
    print("Conversion failed")
```

## User Interface

The Morse Code Converter application provides several functions for handling user interaction.

**Module**: `morse_code.ui`

### Functions

#### get_user_choice

```python
def get_user_choice() -> str
```

Get a valid menu choice from the user.

- **Returns**:
    - str: A string representing the user's choice ('1', '2', '3', or '4').

#### get_yes_or_no

```python
def get_yes_or_no(prompt: str) -> bool
```

Get a yes or no response from the user.

- **Parameters**:
    - `prompt` (str): The prompt to display to the user.
- **Returns**:
    - bool: True if the user answered yes, False if the user answered no.

#### display_menu

```python
def display_menu() -> None
```

Display the main menu of the application.

#### display_welcome_message

```python
def display_welcome_message() -> None
```

Display the welcome message of the application.

#### display_goodbye_message

```python
def display_goodbye_message() -> None
```

Display the goodbye message of the application.

## Logging

The Morse Code Converter application provides a centralized logging system.

**Module**: `morse_code.logging_config`

### Functions

#### get_logger

```python
def get_logger(name)
```

Get a logger with the specified name.

- **Parameters**:
    - `name` (str): The name of the logger, typically the module name.
- **Returns**:
    - logging.Logger: A configured logger instance.

#### Convenience Functions

```python
def debug(message)


    def info(message)


    def warning(message)


    def error(message)


    def critical(message)


    def exception(message)
```

These functions provide convenient ways to log messages at different levels.

## Morse Code Data

The Morse Code Converter application provides dictionaries that map characters to their corresponding Morse code
representations.

**Module**: `morse_code.morse_code_data`

### Dictionaries

#### international_code

```python
international_code = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    # ... more characters
}
```

A dictionary mapping characters to their Morse code representations according to the International Morse code standard (
ITU).

## Usage Examples

### Basic Usage

```python
from morse_code import MorseCodeConverterFactory, MorseCodePlayer

# Create a converter
converter = MorseCodeConverterFactory.create_converter()

# Convert text to Morse code
morse_code = converter.to_morse_code("HELLO WORLD")
print(morse_code)  # Output: ".... . .-.. .-.. ---     .-- --- .-. .-.. -.."

# Convert Morse code to text
text = converter.from_morse_code(".... . .-.. .-.. ---     .-- --- .-. .-.. -..")
print(text)  # Output: "HELLO WORLD"

# Play Morse code as audio
player = MorseCodePlayer()
player.play_morse_code(morse_code)
```

### Error Handling

```python
from morse_code import MorseCodeConverterFactory, safe_execute, InputError

# Create a converter
converter = MorseCodeConverterFactory.create_converter()

try:
    # Try to convert an empty string
    morse_code = converter.to_morse_code("")
except InputError as e:
    print(f"Error: {e}")  # Output: "Error: Input Error: input_string cannot be empty"

# Using safe_execute
morse_code = safe_execute(converter.to_morse_code, "", default_return="")
if not morse_code:
    print("Conversion failed")  # Output: "Conversion failed"
```

### Custom Morse Code Variant

```python
from morse_code import MorseCodeConverterFactory

# Create a custom Morse code variant
custom_code = {
    'A': '.-', 'B': '-...', 'C': '-.-.',
    # ... more characters
}

# Register the custom variant
MorseCodeConverterFactory.register_variant('custom', custom_code)

# Create a converter using the custom variant
converter = MorseCodeConverterFactory.create_converter('custom')

# Use the converter
morse_code = converter.to_morse_code("HELLO")
print(morse_code)
```

### Custom Audio Parameters

```python
from morse_code import MorseCodePlayer

# Create a player with custom audio parameters
player = MorseCodePlayer(frequency=800, unit_duration=150)

# Play Morse code with the custom parameters
player.play_morse_code(".... . .-.. .-.. ---")  # Plays "HELLO" in Morse code
```