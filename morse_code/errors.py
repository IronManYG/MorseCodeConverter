"""
Error handling module for the Morse Code Converter application.

This module provides custom exception classes and error handling utilities
for the Morse Code Converter application.
"""

from .logging_config import get_logger

# Create a logger for this module
logger = get_logger(__name__)


class MorseCodeError(Exception):
    """Base exception class for all Morse Code Converter errors."""

    def __init__(self, message="An error occurred in the Morse Code Converter"):
        self.message = message
        super().__init__(self.message)
        logger.error(f"MorseCodeError: {message}")


class InputError(MorseCodeError):
    """Exception raised for errors in the input."""

    def __init__(self, message="Invalid input provided"):
        super().__init__(f"Input Error: {message}")


class ConversionError(MorseCodeError):
    """Exception raised for errors during conversion."""

    def __init__(self, message="Error during conversion"):
        super().__init__(f"Conversion Error: {message}")


class AudioError(MorseCodeError):
    """Exception raised for errors related to audio playback."""

    def __init__(self, message="Error during audio playback"):
        super().__init__(f"Audio Error: {message}")


class ConfigurationError(MorseCodeError):
    """Exception raised for errors in configuration."""

    def __init__(self, message="Error in configuration"):
        super().__init__(f"Configuration Error: {message}")


def handle_error(error, default_return=None):
    """
    Handle an error by logging it and returning a default value.
    
    This function logs the error and returns a default value, allowing
    the application to continue running despite the error.
    
    Args:
        error (Exception): The error to handle.
        default_return: The value to return if an error occurs. Default is None.
        
    Returns:
        The default return value.
    """
    logger.error(f"Error handled: {str(error)}")
    return default_return


def safe_execute(func, *args, default_return=None, **kwargs):
    """
    Execute a function safely, handling any exceptions.
    
    This function executes the given function with the provided arguments,
    catching and handling any exceptions that occur.
    
    Args:
        func (callable): The function to execute.
        *args: Positional arguments to pass to the function.
        default_return: The value to return if an error occurs. Default is None.
        **kwargs: Keyword arguments to pass to the function.
        
    Returns:
        The result of the function call, or the default return value if an error occurs.
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return handle_error(e, default_return)
