# Morse Code Converter User Guide

## Table of Contents

1. [Introduction](#introduction)
    - [What is Morse Code?](#what-is-morse-code)
    - [History of Morse Code](#history-of-morse-code)
    - [How Morse Code Works](#how-morse-code-works)
2. [Getting Started](#getting-started)
    - [System Requirements](#system-requirements)
    - [Installation](#installation)
    - [Running the Application](#running-the-application)
3. [Using the Application](#using-the-application)
    - [Main Menu](#main-menu)
    - [Converting Text to Morse Code](#converting-text-to-morse-code)
    - [Converting Morse Code to Text](#converting-morse-code-to-text)
    - [Playing Morse Code Sound](#playing-morse-code-sound)
    - [Exiting the Application](#exiting-the-application)
4. [Advanced Usage](#advanced-usage)
    - [Using the API Programmatically](#using-the-api-programmatically)
    - [Creating Custom Morse Code Variants](#creating-custom-morse-code-variants)
    - [Customizing Audio Parameters](#customizing-audio-parameters)
5. [Troubleshooting](#troubleshooting)
    - [Common Issues](#common-issues)
    - [Error Messages](#error-messages)
    - [Logging](#logging)
6. [Reference](#reference)
    - [International Morse Code Chart](#international-morse-code-chart)
    - [Morse Code Timing](#morse-code-timing)
    - [Command-Line Arguments](#command-line-arguments)

## Introduction

### What is Morse Code?

Morse code is a method of transmitting text information as a series of on-off tones, lights, or clicks that can be
directly understood by a skilled listener or observer without special equipment. It is named after Samuel F. B. Morse,
an inventor of the telegraph.

The basic elements of Morse code are:

- **Dot (.)**: A short signal, often represented as a "dit" in sound
- **Dash (-)**: A longer signal, often represented as a "dah" in sound
- **Space**: Used to separate characters and words

### History of Morse Code

Morse code was developed in the 1830s and 1840s by Samuel Morse and Alfred Vail for use with the telegraph. The original
Morse code was designed for the American telegraph system and was later refined into the International Morse Code (also
known as Continental Morse Code) that is still in use today.

Morse code was widely used for communication before the advent of voice transmission and remained a critical method for
maritime communication until the late 20th century. Today, it is still used by amateur radio operators, as an assistive
technology for people with disabilities, and in certain specialized fields.

### How Morse Code Works

In Morse code, each letter, number, and special character is represented by a unique sequence of dots and dashes. For
example:

- The letter 'A' is represented as `.-`
- The letter 'B' is represented as `-...`
- The number '1' is represented as `.----`

When transmitting Morse code, the timing is crucial:

- A dash is three times as long as a dot
- The space between elements (dots and dashes) within a character is equal to one dot
- The space between characters is equal to three dots
- The space between words is equal to seven dots

This timing ensures that the code can be accurately interpreted by the receiver.

## Getting Started

### System Requirements

To run the Morse Code Converter application, you need:

- Python 3.6 or higher
- pygame library (for audio playback)
- A system capable of audio output (for playing Morse code sounds)

### Installation

1. Clone the repository or download the source code.

2. Install the required dependencies:

   ```bash
   pip install pygame
   ```

3. No additional build steps are required as this is a pure Python project.

### Running the Application

To start the application, navigate to the project directory and run:

```bash
python main.py
```

This will launch the application and display the welcome message and main menu.

## Using the Application

### Main Menu

When you start the application, you'll see the main menu with the following options:

```
Welcome to the International Morse Code Converter and Player

Options:
1. Convert Text to Morse Code and Optionally Play Sound
2. Convert Morse Code to Text and Optionally Play Sound
3. Play Morse Code Sound
4. Exit
Choose an option (1-4):
```

Enter the number corresponding to your choice and press Enter.

### Converting Text to Morse Code

To convert text to Morse code:

1. Select option 1 from the main menu.
2. Enter the text you want to convert when prompted.
3. The application will display the Morse code representation of your text.
4. You'll be asked if you want to play the Morse code sound. Enter 'y' or 'yes' to play the sound, or 'n' or 'no' to
   return to the main menu.

**Example:**

```
Choose an option (1-4): 1
Write your message to convert to Morse Code: HELLO WORLD
Your Morse code: .... . .-.. .-.. ---     .-- --- .-. .-.. -..
Do you want to play the Morse code sound? (Yes/No): yes
```

**Notes:**

- The application converts all text to uppercase before conversion.
- Characters that don't have a Morse code representation will be ignored with a warning.
- Spaces between words in your text will be represented as three spaces in the Morse code.

### Converting Morse Code to Text

To convert Morse code to text:

1. Select option 2 from the main menu.
2. Enter the Morse code you want to convert when prompted.
3. The application will display the text representation of your Morse code.
4. You'll be asked if you want to play the Morse code sound. Enter 'y' or 'yes' to play the sound, or 'n' or 'no' to
   return to the main menu.

**Example:**

```
Choose an option (1-4): 2
Enter Morse Code to convert to Text: ... --- ...
Your text message: SOS
Do you want to play the Morse code sound? (Yes/No): no
```

**Notes:**

- Morse code should be entered with dots (.), dashes (-), and spaces.
- Characters within a word should be separated by a single space.
- Words should be separated by three spaces.
- Invalid Morse code characters will result in an error message.

### Playing Morse Code Sound

To play Morse code sound without conversion:

1. Select option 3 from the main menu.
2. Enter the Morse code you want to play when prompted.
3. The application will play the Morse code sound.

**Example:**

```
Choose an option (1-4): 3
Enter Morse Code to play as sound: .- -... -.-.
```

**Notes:**

- The application will validate the Morse code input to ensure it contains only valid characters (dots, dashes, and
  spaces).
- The sound will play according to standard Morse code timing conventions.

### Exiting the Application

To exit the application:

1. Select option 4 from the main menu.
2. The application will display a goodbye message and terminate.

**Example:**

```
Choose an option (1-4): 4
Thank you for using the Morse Code Converter and Player!
```

## Advanced Usage

### Using the API Programmatically

You can use the Morse Code Converter API programmatically in your own Python code:

```python
from morse_code import MorseCodeConverterFactory, MorseCodePlayer, international_code

# Create a converter using the factory
converter = MorseCodeConverterFactory.create_converter()

# Convert text to Morse code
morse_code = converter.to_morse_code("HELLO WORLD")
print(morse_code)  # Output: .... . .-.. .-.. ---     .-- --- .-. .-.. -..

# Convert Morse code to text
text = converter.from_morse_code("... --- ...")
print(text)  # Output: SOS

# Play Morse code as audio
player = MorseCodePlayer()
player.play_morse_code("... --- ...")

# You can also create a converter directly if you prefer
from morse_code import MorseCodeConverter

direct_converter = MorseCodeConverter(international_code)
```

### Creating Custom Morse Code Variants

You can create and register custom Morse code variants:

```python
from morse_code import MorseCodeConverterFactory

# Create a custom Morse code variant
custom_code = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    # Add more characters as needed
}

# Register the custom variant
MorseCodeConverterFactory.register_variant('custom', custom_code)

# Create a converter using the custom variant
converter = MorseCodeConverterFactory.create_converter('custom')

# Use the converter
morse_code = converter.to_morse_code("HELLO")
print(morse_code)
```

### Customizing Audio Parameters

You can customize the audio parameters when creating a MorseCodePlayer:

```python
from morse_code import MorseCodePlayer

# Create a player with custom audio parameters
player = MorseCodePlayer(
    frequency=800,  # Hz (default is 600)
    unit_duration=150  # ms (default is 100)
)

# Play Morse code with the custom parameters
player.play_morse_code("... --- ...")
```

## Troubleshooting

### Common Issues

#### No Sound

If you don't hear any sound when playing Morse code:

1. Check that your system's audio is working and not muted.
2. Ensure that pygame is properly installed (`pip install pygame`).
3. Try increasing the frequency or unit duration when creating the MorseCodePlayer.

#### Invalid Input Errors

If you receive errors about invalid input:

1. For text to Morse code conversion, ensure you're using characters that have Morse code representations (letters,
   numbers, and some special characters).
2. For Morse code to text conversion, ensure you're using only dots (.), dashes (-), and spaces.
3. Make sure you're using the correct spacing: one space between characters, three spaces between words.

### Error Messages

The application provides descriptive error messages to help you identify and resolve issues:

- **"Input Error: input_string cannot be empty"**: You must provide a non-empty string for conversion.
- **"Input Error: morse_string contains invalid characters"**: Your Morse code input contains characters other than
  dots, dashes, and spaces.
- **"Audio Error: Failed to initialize pygame mixer"**: There was an issue initializing the audio system.

### Logging

The application logs detailed information about its operation, which can be helpful for troubleshooting:

1. Log files are stored in the `logs` directory.
2. Each log file is named with a timestamp (e.g., `morse_code_20250801_123456.log`).
3. The logs contain information about application startup, user actions, errors, and more.

To view the logs:

1. Navigate to the `logs` directory.
2. Open the most recent log file in a text editor.
3. Look for ERROR or WARNING entries that might indicate issues.

## Reference

### International Morse Code Chart

#### Letters

| Letter | Morse Code |
|--------|------------|
| A      | .-         |
| B      | -...       |
| C      | -.-.       |
| D      | -..        |
| E      | .          |
| F      | ..-.       |
| G      | --.        |
| H      | ....       |
| I      | ..         |
| J      | .---       |
| K      | -.-        |
| L      | .-..       |
| M      | --         |
| N      | -.         |
| O      | ---        |
| P      | .--.       |
| Q      | --.-       |
| R      | .-.        |
| S      | ...        |
| T      | -          |
| U      | ..-        |
| V      | ...-       |
| W      | .--        |
| X      | -..-       |
| Y      | -.--       |
| Z      | --..       |

#### Numbers

| Number | Morse Code |
|--------|------------|
| 0      | -----      |
| 1      | .----      |
| 2      | ..---      |
| 3      | ...--      |
| 4      | ....-      |
| 5      | .....      |
| 6      | -....      |
| 7      | --...      |
| 8      | ---..      |
| 9      | ----.      |

#### Special Characters

| Character | Morse Code |
|-----------|------------|
| .         | .-.-.-     |
| ,         | --..--     |
| ?         | ..--..     |
| '         | .----.     |
| !         | -.-.--     |
| /         | -..-.      |
| (         | -.--.      |
| )         | -.--.-     |
| &         | .-...      |
| :         | ---...     |
| ;         | -.-.-.     |
| =         | -...-      |
| +         | .-.-.      |
| -         | -....-     |
| _         | ..--.-     |
| "         | .-..-.     |
| $         | ...-..-    |
| @         | .--.-.     |

### Morse Code Timing

The timing in Morse code is based on the duration of a dot:

- Dot: 1 unit
- Dash: 3 units
- Space between elements (dots and dashes) within a character: 1 unit
- Space between characters: 3 units
- Space between words: 7 units

In the Morse Code Converter application, these timings are configurable through the `MORSE_TIMING` dictionary in the
`config.py` file.

### Command-Line Arguments

Currently, the application does not support command-line arguments. All options are selected through the interactive
menu after starting the application.

Future versions may include command-line arguments for direct conversion and playback without using the interactive
menu.