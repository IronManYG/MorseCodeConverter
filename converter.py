class MorseCodeConverter:
    def __init__(self, morse_code_dict):
        self.morse_code_dict = morse_code_dict

    def to_morse_code(self, input_string):
        """
        Converts a string to Morse code, ignoring characters not in the Morse code dictionary.

        Args:
        input_string (str): The string to convert.
        morse_code_dict (dict): The Morse code dictionary.

        Returns:
        str: The converted Morse code string.
        """
        upper_string = input_string.upper()
        morse_code_list = []

        for char in upper_string:
            if char in self.morse_code_dict:
                morse_code_list.append(self.morse_code_dict[char])
            elif char == ' ':
                morse_code_list.append('   ')  # Three spaces to separate words in Morse code
            else:
                # Optionally, you can print a warning or ignore the character
                print(f"Warning: '{char}' is not a valid Morse code character and will be ignored.")

        return ' '.join(morse_code_list)

    def from_morse_code(self, morse_string):
        # Invert the Morse code dictionary
        text_dict = {v: k for k, v in self.morse_code_dict.items()}

        # Split the Morse code string into words and then characters
        morse_words = morse_string.split('   ')  # Three spaces to separate words
        decoded_message = []

        for word in morse_words:
            decoded_chars = [text_dict[char] for char in word.split() if char in text_dict]
            decoded_message.append(''.join(decoded_chars))

        return ' '.join(decoded_message)
