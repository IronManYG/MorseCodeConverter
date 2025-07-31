"""
User interface module for the Morse Code Converter application.

This module provides functions for handling user interaction in the
Morse Code Converter application, including menu display and input validation.
"""

from .config import UI_CONFIG, VALIDATION_CONFIG


def get_user_choice():
    """
    Get a valid menu choice from the user.
    
    This function prompts the user to enter a choice between 1 and 4,
    and validates the input to ensure it's a valid option.
    
    Returns:
        str: A string representing the user's choice ('1', '2', '3', or '4').
    """
    valid_choices = VALIDATION_CONFIG['valid_menu_choices']
    while True:
        choice = input("Choose an option (1-4): ")
        if choice in valid_choices:
            return choice
        else:
            print(f"Invalid option, please choose a number between {min(valid_choices)} and {max(valid_choices)}.")


def get_yes_or_no(prompt):
    """
    Get a yes or no response from the user.
    
    This function prompts the user with the given prompt and validates
    the input to ensure it's a valid yes or no response.
    
    Args:
        prompt (str): The prompt to display to the user.
        
    Returns:
        bool: True if the user answered yes, False if the user answered no.
    """
    valid_yes = VALIDATION_CONFIG['valid_yes_responses']
    valid_no = VALIDATION_CONFIG['valid_no_responses']

    while True:
        response = input(prompt).lower()
        if response in valid_yes:
            return True
        elif response in valid_no:
            return False
        else:
            print(f"Please answer with '{list(valid_yes)[0]}' or '{list(valid_no)[0]}'.")


def display_menu():
    """
    Display the main menu of the application.
    
    This function prints the available options to the console.
    """
    print("\nOptions:")
    for option in UI_CONFIG['menu_options']:
        print(option)


def display_welcome_message():
    """
    Display the welcome message of the application.
    
    This function prints the welcome message to the console.
    """
    print(UI_CONFIG['welcome_message'])


def display_goodbye_message():
    """
    Display the goodbye message of the application.
    
    This function prints the goodbye message to the console.
    """
    print(UI_CONFIG['goodbye_message'])
