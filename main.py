"""
Main module for the Morse Code Converter application.

This module provides a command-line interface for converting text to Morse code,
converting Morse code to text, and playing Morse code as audio.
"""

from morse_code import (
    MorseCodeConverterFactory,
    MorseCodePlayer,
    get_user_choice,
    get_yes_or_no,
    display_menu,
    display_welcome_message,
    display_goodbye_message,
    get_logger,
    DEFAULT_MORSE_VARIANT
)

# Create a logger for this module
logger = get_logger(__name__)


def main():
    """
    Main function that runs the Morse Code Converter application.
    
    This function initializes the converter and player, displays the menu,
    and handles user input to perform the requested operations.
    """
    logger.info("Starting Morse Code Converter application")

    try:
        # Initialize components
        international_converter = MorseCodeConverterFactory.create_converter(DEFAULT_MORSE_VARIANT)
        player = MorseCodePlayer()
        logger.debug(f"Initialized converter for {DEFAULT_MORSE_VARIANT} variant and player")

        display_welcome_message()

        convert_message = True
        while convert_message:
            display_menu()
            choice = get_user_choice()
            logger.debug(f"User selected option {choice}")

            if choice == '1':
                message = input("Write your message to convert to Morse Code: ")
                logger.debug(f"Converting text to Morse code: {message}")
                morse_message = international_converter.to_morse_code(message)
                print(f"Your Morse code: {morse_message}")

                if get_yes_or_no("Do you want to play the Morse code sound? (Yes/No): "):
                    logger.debug("Playing Morse code as audio")
                    player.play_morse_code(morse_message)
                    logger.info("Sound playback finished.")

            elif choice == '2':
                morse_code = input("Enter Morse Code to convert to Text: ")
                logger.debug(f"Converting Morse code to text: {morse_code}")
                text_message = international_converter.from_morse_code(morse_code)
                print(f"Your text message: {text_message}")

                if get_yes_or_no("Do you want to play the Morse code sound? (Yes/No): "):
                    logger.debug("Playing Morse code as audio")
                    player.play_morse_code(morse_code)
                    logger.info("Sound playback finished.")

            elif choice == '3':
                morse_code = input("Enter Morse Code to play as sound: ")
                logger.debug(f"Playing Morse code as audio: {morse_code}")
                player.play_morse_code(morse_code)
                logger.info("Sound playback finished.")

            elif choice == '4':
                logger.debug("User chose to exit")
                convert_message = False

        display_goodbye_message()
        logger.info("Morse Code Converter application shutting down")

    except Exception as e:
        logger.exception(f"An error occurred: {str(e)}")
        print("An error occurred. Please check the logs for details.")


if __name__ == "__main__":
    main()
