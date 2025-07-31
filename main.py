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
    DEFAULT_MORSE_VARIANT,
    InputError,
    VALIDATION_CONFIG,
    safe_execute
)

# Create a logger for this module
logger = get_logger(__name__)


def main() -> None:
    """
    Main function that runs the Morse Code Converter application.
    
    This function initializes the converter and player, displays the menu,
    and handles user input to perform the requested operations.
    
    Returns:
        None
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
            try:
                display_menu()
                choice = get_user_choice()
                logger.debug(f"User selected option {choice}")

                if choice == '1':
                    # Text to Morse code conversion
                    message = input("Write your message to convert to Morse Code: ")
                    if not message:
                        raise InputError("Message cannot be empty")

                    logger.debug(f"Converting text to Morse code: {message}")
                    morse_message = safe_execute(
                        international_converter.to_morse_code,
                        message,
                        default_return=None
                    )

                    if morse_message is None:
                        print("Failed to convert text to Morse code. Please try again.")
                        continue

                    print(f"Your Morse code: {morse_message}")

                    if get_yes_or_no("Do you want to play the Morse code sound? (Yes/No): "):
                        logger.debug("Playing Morse code as audio")
                        safe_execute(player.play_morse_code, morse_message)
                        logger.info("Sound playback finished.")

                elif choice == '2':
                    # Morse code to text conversion
                    morse_code = input("Enter Morse Code to convert to Text: ")
                    if not morse_code:
                        raise InputError("Morse code cannot be empty")

                    # Validate Morse code characters
                    valid_chars = VALIDATION_CONFIG['valid_morse_chars']
                    invalid_chars = [char for char in morse_code if char not in valid_chars]
                    if invalid_chars:
                        unique_invalid = set(invalid_chars)
                        raise InputError(
                            f"Invalid characters in Morse code: {', '.join(unique_invalid)}. "
                            f"Only dots (.), dashes (-), and spaces are allowed."
                        )

                    logger.debug(f"Converting Morse code to text: {morse_code}")
                    text_message = safe_execute(
                        international_converter.from_morse_code,
                        morse_code,
                        default_return=None
                    )

                    if text_message is None:
                        print("Failed to convert Morse code to text. Please try again.")
                        continue

                    print(f"Your text message: {text_message}")

                    if get_yes_or_no("Do you want to play the Morse code sound? (Yes/No): "):
                        logger.debug("Playing Morse code as audio")
                        safe_execute(player.play_morse_code, morse_code)
                        logger.info("Sound playback finished.")

                elif choice == '3':
                    # Play Morse code as sound
                    morse_code = input("Enter Morse Code to play as sound: ")
                    if not morse_code:
                        raise InputError("Morse code cannot be empty")

                    # Validate Morse code characters
                    valid_chars = VALIDATION_CONFIG['valid_morse_chars']
                    invalid_chars = [char for char in morse_code if char not in valid_chars]
                    if invalid_chars:
                        unique_invalid = set(invalid_chars)
                        raise InputError(
                            f"Invalid characters in Morse code: {', '.join(unique_invalid)}. "
                            f"Only dots (.), dashes (-), and spaces are allowed."
                        )

                    logger.debug(f"Playing Morse code as audio: {morse_code}")
                    safe_execute(player.play_morse_code, morse_code)
                    logger.info("Sound playback finished.")

                elif choice == '4':
                    logger.debug("User chose to exit")
                    convert_message = False

            except InputError as e:
                logger.warning(f"Input error: {str(e)}")
                print(f"Error: {str(e)}")
                print("Please try again.")
            except Exception as e:
                logger.error(f"Error during operation: {str(e)}")
                print(f"An error occurred: {str(e)}")
                print("Please try again.")

        display_goodbye_message()
        logger.info("Morse Code Converter application shutting down")

    except KeyboardInterrupt:
        logger.info("Application terminated by user (KeyboardInterrupt)")
        print("\nApplication terminated by user.")
        display_goodbye_message()
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {str(e)}")
        print(f"An unexpected error occurred: {str(e)}")
        print("The application will now exit.")
    finally:
        # Ensure resources are properly released
        try:
            # Clean up pygame resources if needed
            import pygame
            pygame.quit()
            logger.debug("Pygame resources released")
        except Exception as e:
            logger.warning(f"Error during cleanup: {str(e)}")


if __name__ == "__main__":
    main()
