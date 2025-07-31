"""
Test script to verify error handling improvements in the MorseCodeConverter class.
"""
from morse_code import MorseCodeConverter, international_code


def test_converter_initialization():
    """Test initialization with invalid input."""
    print("\nTesting converter initialization...")

    # Valid initialization
    try:
        converter = MorseCodeConverter(international_code)
        print("✓ Valid initialization successful")
    except Exception as e:
        print(f"✗ Valid initialization failed: {e}")

    # Invalid initialization (not a dictionary)
    try:
        converter = MorseCodeConverter("not a dictionary")
        print("✗ Invalid initialization did not raise an exception")
    except TypeError as e:
        print(f"✓ Invalid initialization correctly raised TypeError: {e}")
    except Exception as e:
        print(f"✗ Invalid initialization raised unexpected exception: {e}")


def test_to_morse_code():
    """Test to_morse_code method with various inputs."""
    print("\nTesting to_morse_code method...")
    converter = MorseCodeConverter(international_code)

    # Valid input
    try:
        result = converter.to_morse_code("SOS")
        print(f"✓ Valid input conversion successful: {result}")
    except Exception as e:
        print(f"✗ Valid input conversion failed: {e}")

    # Input with invalid characters
    try:
        result = converter.to_morse_code("Hello, World! 123")
        print(f"✓ Input with invalid characters handled: {result}")
    except Exception as e:
        print(f"✗ Input with invalid characters failed: {e}")

    # Empty input
    try:
        result = converter.to_morse_code("")
        print(f"✗ Empty input did not raise an exception")
    except MorseCodeConverter.InvalidInputError as e:
        print(f"✓ Empty input correctly raised InvalidInputError: {e}")
    except Exception as e:
        print(f"✗ Empty input raised unexpected exception: {e}")

    # Non-string input
    try:
        result = converter.to_morse_code(123)
        print(f"✗ Non-string input did not raise an exception")
    except TypeError as e:
        print(f"✓ Non-string input correctly raised TypeError: {e}")
    except Exception as e:
        print(f"✗ Non-string input raised unexpected exception: {e}")


def test_from_morse_code():
    """Test from_morse_code method with various inputs."""
    print("\nTesting from_morse_code method...")
    converter = MorseCodeConverter(international_code)

    # Valid input
    try:
        result = converter.from_morse_code("... --- ...")
        print(f"✓ Valid input conversion successful: {result}")
    except Exception as e:
        print(f"✗ Valid input conversion failed: {e}")

    # Input with invalid Morse codes
    try:
        result = converter.from_morse_code("... --- ... .... .....")
        print(f"✓ Input with invalid Morse codes handled: {result}")
    except Exception as e:
        print(f"✗ Input with invalid Morse codes failed: {e}")

    # Empty input
    try:
        result = converter.from_morse_code("")
        print(f"✗ Empty input did not raise an exception")
    except MorseCodeConverter.InvalidInputError as e:
        print(f"✓ Empty input correctly raised InvalidInputError: {e}")
    except Exception as e:
        print(f"✗ Empty input raised unexpected exception: {e}")

    # Non-string input
    try:
        result = converter.from_morse_code(123)
        print(f"✗ Non-string input did not raise an exception")
    except TypeError as e:
        print(f"✓ Non-string input correctly raised TypeError: {e}")
    except Exception as e:
        print(f"✗ Non-string input raised unexpected exception: {e}")

    # Input with invalid characters
    try:
        result = converter.from_morse_code("... --- ... !")
        print(f"✗ Input with invalid characters did not raise an exception")
    except MorseCodeConverter.InvalidInputError as e:
        print(f"✓ Input with invalid characters correctly raised InvalidInputError: {e}")
    except Exception as e:
        print(f"✗ Input with invalid characters raised unexpected exception: {e}")


if __name__ == "__main__":
    print("Testing error handling in MorseCodeConverter class...")
    test_converter_initialization()
    test_to_morse_code()
    test_from_morse_code()
    print("\nAll tests completed.")
