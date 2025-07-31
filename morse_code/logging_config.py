"""
Logging configuration module for the Morse Code Converter application.

This module provides a centralized logging configuration for the Morse Code Converter
application, including log formatters, handlers, and convenience functions.
"""

import logging
import os
import sys
from datetime import datetime

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(logs_dir, exist_ok=True)

# Configure the root logger
logger = logging.getLogger('morse_code')
logger.setLevel(logging.DEBUG)

# Create formatters
console_formatter = logging.Formatter('%(levelname)s: %(message)s')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(console_formatter)

# Create file handler
log_file = os.path.join(logs_dir, f'morse_code_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)


def get_logger(name):
    """
    Get a logger with the specified name.
    
    This function returns a logger that is a child of the root 'morse_code' logger,
    inheriting its configuration.
    
    Args:
        name (str): The name of the logger, typically the module name.
        
    Returns:
        logging.Logger: A configured logger instance.
    """
    return logging.getLogger(f'morse_code.{name}')


# Convenience functions for logging
def debug(message):
    """Log a debug message."""
    logger.debug(message)


def info(message):
    """Log an info message."""
    logger.info(message)


def warning(message):
    """Log a warning message."""
    logger.warning(message)


def error(message):
    """Log an error message."""
    logger.error(message)


def critical(message):
    """Log a critical message."""
    logger.critical(message)


def exception(message):
    """Log an exception message with traceback."""
    logger.exception(message)
