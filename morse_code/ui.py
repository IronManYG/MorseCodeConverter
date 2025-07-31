"""
User interface module for the Morse Code Converter application.

This module provides functions for handling user interaction in the
Morse Code Converter application, including menu display and input validation.
"""

from typing import Set

from .config import UI_CONFIG, VALIDATION_CONFIG, COLORS


def colorize(text: str, color: str, bold: bool = False, underline: bool = False) -> str:
    """
    Apply color and style to text.
    
    Args:
        text (str): The text to colorize.
        color (str): The color to apply (must be a key in the COLORS dictionary).
        bold (bool, optional): Whether to make the text bold. Defaults to False.
        underline (bool, optional): Whether to underline the text. Defaults to False.
        
    Returns:
        str: The colorized text.
    """
    style = ""
    if color in COLORS:
        style += COLORS[color]
    if bold:
        style += COLORS['BOLD']
    if underline:
        style += COLORS['UNDERLINE']

    return f"{style}{text}{COLORS['RESET']}"


def colorize_header(text: str) -> str:
    """
    Apply header styling to text.
    
    Args:
        text (str): The text to style as a header.
        
    Returns:
        str: The styled header text.
    """
    return colorize(text, 'CYAN', bold=True)


def colorize_result(text: str) -> str:
    """
    Apply result styling to text.
    
    Args:
        text (str): The text to style as a result.
        
    Returns:
        str: The styled result text.
    """
    return colorize(text, 'GREEN')


def colorize_error(text: str) -> str:
    """
    Apply error styling to text.
    
    Args:
        text (str): The text to style as an error.
        
    Returns:
        str: The styled error text.
    """
    return colorize(text, 'RED', bold=True)


def colorize_warning(text: str) -> str:
    """
    Apply warning styling to text.
    
    Args:
        text (str): The text to style as a warning.
        
    Returns:
        str: The styled warning text.
    """
    return colorize(text, 'YELLOW')


def get_user_choice() -> str:
    """
    Get a valid menu choice from the user.
    
    This function prompts the user to enter a choice between 1 and 4,
    and validates the input to ensure it's a valid option.
    
    Returns:
        str: A string representing the user's choice ('1', '2', '3', or '4').
    """
    valid_choices: Set[str] = VALIDATION_CONFIG['valid_menu_choices']
    while True:
        choice: str = input("Choose an option (1-4): ")
        if choice in valid_choices:
            return choice
        else:
            print(f"Invalid option, please choose a number between {min(valid_choices)} and {max(valid_choices)}.")


def get_yes_or_no(prompt: str) -> bool:
    """
    Get a yes or no response from the user.
    
    This function prompts the user with the given prompt and validates
    the input to ensure it's a valid yes or no response.
    
    Args:
        prompt (str): The prompt to display to the user.
        
    Returns:
        bool: True if the user answered yes, False if the user answered no.
    """
    valid_yes: Set[str] = VALIDATION_CONFIG['valid_yes_responses']
    valid_no: Set[str] = VALIDATION_CONFIG['valid_no_responses']

    while True:
        response: str = input(prompt).lower()
        if response in valid_yes:
            return True
        elif response in valid_no:
            return False
        else:
            print(f"Please answer with '{list(valid_yes)[0]}' or '{list(valid_no)[0]}'.")


def display_menu() -> None:
    """
    Display the main menu of the application.
    
    This function prints the available options to the console with improved formatting and colors.
    
    Returns:
        None
    """
    print(colorize_header(UI_CONFIG['menu_header']))
    for option in UI_CONFIG['menu_options']:
        # Highlight the option number in cyan
        parts = option.split('. ', 1)
        if len(parts) == 2:
            number, text = parts
            print(f"  {colorize(number, 'CYAN', bold=True)}. {text}")
        else:
            print(f"  {option}")
    print(UI_CONFIG['section_separator'])


def display_welcome_message() -> None:
    """
    Display the welcome message of the application.
    
    This function prints the welcome message to the console with colors.
    
    Returns:
        None
    """
    print(colorize(UI_CONFIG['welcome_message'], 'BLUE', bold=True))


def display_goodbye_message() -> None:
    """
    Display the goodbye message of the application.
    
    This function prints the goodbye message to the console with colors.
    
    Returns:
        None
    """
    print(colorize(UI_CONFIG['goodbye_message'], 'BLUE', bold=True))


def display_section_separator() -> None:
    """
    Display a section separator line.
    
    This function prints a separator line to visually separate different sections
    of the application interface with colors.
    
    Returns:
        None
    """
    print(colorize(UI_CONFIG['section_separator'], 'MAGENTA'))


def display_result_header() -> None:
    """
    Display the result header.
    
    This function prints a header for the result section of the application with colors.
    
    Returns:
        None
    """
    print(colorize_result(UI_CONFIG['result_header']))


def format_result(label: str, value: str) -> str:
    """
    Format a result with a label and value.
    
    This function formats a result with a label and value for display with colors.
    
    Args:
        label (str): The label for the result.
        value (str): The value of the result.
        
    Returns:
        str: The formatted result string.
    """
    return f"  {colorize(label, 'YELLOW', bold=True)}: {colorize(value, 'GREEN')}"
