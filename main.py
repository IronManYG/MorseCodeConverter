from converter import MorseCodeConverter
from morse_code_player import MorseCodePlayer
from morse_code_data import international_code  # Import the dictionary

international_converter = MorseCodeConverter(international_code)
player = MorseCodePlayer()

print('Welcome to the International Morse Code Converter')

convert_message = True
while convert_message:
    message = input("Write your message: ")
    morse_message = international_converter.to_morse_code(message)
    print(f"Your Morse code: {morse_message}")
    player.play_morse_code(morse_message)

    continue_input = input("Do you want to convert another message? (Yes/No): ").lower()
    if continue_input not in ['y', 'yes']:
        convert_message = False
