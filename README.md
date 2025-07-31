# International Morse Code Converter and Player

## Project Overview
The International Morse Code Converter and Player is a Python-based application that allows users to convert text to Morse code and vice versa, and to play Morse code sounds. This project combines data processing and audio manipulation to create an interactive tool for both Morse code enthusiasts and learners.

## Features
- **Text to Morse Code Conversion**: Convert any text into its Morse code representation.
- **Morse Code to Text Conversion**: Translate Morse code back into readable text.
- **Morse Code Sound Playback**: Play the sound of the Morse code for any given text or Morse code input.
- **Interactive Console Menu**: Easy-to-navigate options for all functionalities.
- **Error Handling**: Comprehensive error handling for invalid inputs and edge cases.
- **Logging System**: Detailed logging for debugging and tracking application behavior.
- **Extensible Design**: Support for adding additional Morse code variants.

## Installation

To run this project, ensure you have Python 3.6 or higher installed on your system. Additionally, you need to install
`pygame` for sound playback. Install it using pip:

```bash
pip install pygame
```

## Usage

### Starting the Application

Run `main.py` to start the application:

```bash
python main.py
```

### Navigating the Menu

The application presents a menu with the following options:

1. Convert Text to Morse Code and Optionally Play Sound
2. Convert Morse Code to Text and Optionally Play Sound
3. Play Morse Code Sound
4. Exit

Enter the number corresponding to your choice.

### Usage Examples

#### Example 1: Converting Text to Morse Code

```
Options:
1. Convert Text to Morse Code and Optionally Play Sound
2. Convert Morse Code to Text and Optionally Play Sound
3. Play Morse Code Sound
4. Exit
Choose an option (1-4): 1
Write your message to convert to Morse Code: HELLO WORLD
Your Morse code: .... . .-.. .-.. ---     .-- --- .-. .-.. -..
Do you want to play the Morse code sound? (Yes/No): yes
```

#### Example 2: Converting Morse Code to Text

```
Options:
1. Convert Text to Morse Code and Optionally Play Sound
2. Convert Morse Code to Text and Optionally Play Sound
3. Play Morse Code Sound
4. Exit
Choose an option (1-4): 2
Enter Morse Code to convert to Text: ... --- ...
Your text message: SOS
Do you want to play the Morse code sound? (Yes/No): no
```

#### Example 3: Playing Morse Code Sound

```
Options:
1. Convert Text to Morse Code and Optionally Play Sound
2. Convert Morse Code to Text and Optionally Play Sound
3. Play Morse Code Sound
4. Exit
Choose an option (1-4): 3
Enter Morse Code to play as sound: .- -... -.-.
```

### Using the API Programmatically

You can also use the Morse Code Converter API programmatically in your own Python code:

```python
from morse_code import MorseCodeConverterFactory, MorseCodePlayer

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
```

### Error Handling Examples

The application handles various error scenarios gracefully:

```python
from morse_code import MorseCodeConverterFactory, InputError

converter = MorseCodeConverterFactory.create_converter()

try:
  # This will raise an InputError because the input is empty
  morse_code = converter.to_morse_code("")
except InputError as e:
  print(f"Error: {e}")  # Output: Error: Input Error: input_string cannot be empty

try:
  # This will raise an InputError because the Morse code contains invalid characters
  text = converter.from_morse_code("... --- ... !")
except InputError as e:
  print(
    f"Error: {e}")  # Output: Error: Input Error: morse_string contains invalid characters: !. Only dots (.), dashes (-), and spaces are allowed.
```

## Project Structure

The project is organized into a package structure with the following components:

### Core Modules

- **main.py**: Entry point for the application, contains the command-line interface.
- **morse_code/**: Package containing all the core functionality.
  - **__init__.py**: Package initialization and exports.
  - **converter.py**: Contains the `MorseCodeConverter` class for text-to-morse and morse-to-text conversion.
  - **morse_code_player.py**: Contains the `MorseCodePlayer` class for audio playback.
  - **morse_code_data.py**: Contains the Morse code dictionary mapping characters to their Morse code representations.
  - **factory.py**: Contains the `MorseCodeConverterFactory` class for creating converter instances.
  - **config.py**: Contains configuration settings for the application.
  - **errors.py**: Contains custom exception classes and error handling utilities.
  - **logging_config.py**: Contains logging configuration and utilities.
  - **ui.py**: Contains user interface functions.

### Documentation

- **docs/**: Directory containing documentation files.
  - **api_documentation.md**: Comprehensive API documentation.
  - **plan.md**: Improvement plan for the project.
  - **tasks.md**: Task list for project improvements.

### Logs

- **logs/**: Directory containing log files generated by the application.

## Contributing
Contributions to the International Morse Code Converter and Player are welcome. Feel free to fork the repository and submit pull requests.

For more detailed guidelines, see the CONTRIBUTING.md file (coming soon).

## License

[MIT License](LICENSE.txt) (coming soon)

## Acknowledgments
Special thanks to all contributors and the Python community for their continuous support and inspiration.
