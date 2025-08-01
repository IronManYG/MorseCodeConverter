"""
Test script for the progress indicator in the Morse Code Converter application.

This script tests the progress indicator by playing a long Morse code message.
"""

from morse_code import MorseCodePlayer, MorseCodeConverterFactory, DEFAULT_MORSE_VARIANT


def main():
    """
    Main function to test the progress indicator.
    
    This function creates a long Morse code message and plays it to test the progress indicator.
    """
    print("Testing progress indicator with a long Morse code message...")

    # Create a converter and player
    converter = MorseCodeConverterFactory.create_converter(DEFAULT_MORSE_VARIANT)
    player = MorseCodePlayer()

    # Create a long message
    message = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG 0123456789"

    # Convert to Morse code
    morse_code = converter.to_morse_code(message)

    print(f"Original message: {message}")
    print(f"Morse code: {morse_code}")
    print("\nPlaying Morse code with progress indicator...")

    # Play the Morse code with progress indicator
    player.play_morse_code(morse_code, show_progress=True)

    print("\nTest completed successfully!")


if __name__ == "__main__":
    main()
