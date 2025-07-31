# Morse Code Converter Development Guidelines

This document provides guidelines and instructions for developers working on the Morse Code Converter project.

## Build/Configuration Instructions

### Dependencies

The project requires the following dependencies:

- Python 3.6 or higher
- pygame (for audio playback)

### Installation Steps

1. Clone the repository or download the source code.
2. Install the required dependencies:
   ```
   pip install pygame
   ```
3. No additional build steps are required as this is a pure Python project.

### Project Structure

- `main.py`: Entry point for the application, contains the command-line interface.
- `converter.py`: Contains the `MorseCodeConverter` class for text-to-morse and morse-to-text conversion.
- `morse_code_player.py`: Contains the `MorseCodePlayer` class for audio playback.
- `morse_code_data.py`: Contains the Morse code dictionary mapping characters to their Morse code representations.

## Testing Information

### Running Tests

The project uses Python's built-in `unittest` framework for testing. To run the tests:

```
python test_converter.py
```

This will execute all test cases and report any failures.

### Adding New Tests

1. Create a new test file or add test methods to the existing `test_converter.py` file.
2. Follow the unittest pattern:
    - Create a class that inherits from `unittest.TestCase`
    - Define test methods that start with `test_`
    - Use assertion methods like `assertEqual`, `assertTrue`, etc.
3. Run the tests to ensure they pass.

### Example Test

Here's an example of a test for the Morse code converter:

```python
import unittest
from converter import MorseCodeConverter
from morse_code_data import international_code

class TestMorseCodeConverter(unittest.TestCase):
    def setUp(self):
        self.converter = MorseCodeConverter(international_code)
    
    def test_to_morse_code(self):
        # Test basic conversion
        self.assertEqual(self.converter.to_morse_code("SOS"), "... --- ...")
        
        # Test with spaces
        self.assertEqual(self.converter.to_morse_code("HELLO WORLD"), ".... . .-.. .-.. ---     .-- --- .-. .-.. -..")
        
        # Test with mixed case
        self.assertEqual(self.converter.to_morse_code("Hello"), ".... . .-.. .-.. ---")
        
        # Test with numbers
        self.assertEqual(self.converter.to_morse_code("123"), ".---- ..--- ...--")
        
        # Test with special characters
        self.assertEqual(self.converter.to_morse_code("!?."), "-.-.-- ..--.. .-.-.-")
    
    def test_from_morse_code(self):
        # Test basic conversion
        self.assertEqual(self.converter.from_morse_code("... --- ..."), "SOS")
        
        # Test with word separation
        self.assertEqual(self.converter.from_morse_code(".... . .-.. .-.. ---     .-- --- .-. .-.. -.."), "HELLO WORLD")
        
        # Test with numbers
        self.assertEqual(self.converter.from_morse_code(".---- ..--- ...--"), "123")
        
        # Test with special characters
        self.assertEqual(self.converter.from_morse_code("-.-.-- ..--.. .-.-.-"), "!?.")

if __name__ == '__main__':
    unittest.main()
```

## Code Style and Development Guidelines

### Code Style

- Follow PEP 8 guidelines for Python code style.
- Use meaningful variable and function names.
- Include docstrings for classes and methods.
- Keep functions and methods focused on a single responsibility.

### Error Handling

- Handle potential errors gracefully, especially in user input processing.
- Provide meaningful error messages to users.
- In the converter, characters not in the Morse code dictionary are ignored with a warning.

### Audio Playback

- The `MorseCodePlayer` class uses pygame for audio playback.
- The timing follows standard Morse code conventions:
    - Dot: 1 unit
    - Dash: 3 units
    - Space between elements: 1 unit
    - Space between characters: 3 units
    - Space between words: 7 units

### Extending the Project

To add support for additional Morse code variants:

1. Create a new dictionary in `morse_code_data.py` or a new file.
2. Initialize a new `MorseCodeConverter` instance with the new dictionary.
3. Update the UI in `main.py` to allow selection of the new variant.

To modify the audio playback:

1. Adjust the frequency and unit_duration parameters in the `MorseCodePlayer` constructor.
2. For more advanced changes, modify the `create_sine_wave` and `play_morse_code` methods.

## Debugging Tips

- Use print statements or a debugger to trace the conversion process.
- For audio issues, check that pygame is properly initialized and that the sound parameters are appropriate.
- Test with simple inputs first before moving to more complex cases.
- When modifying the code, run the tests to ensure existing functionality is not broken.