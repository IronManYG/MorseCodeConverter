from converter import MorseCodeConverter
from morse_code_player import MorseCodePlayer
from morse_code_data import international_code  # Import the dictionary

international_converter = MorseCodeConverter(international_code)
player = MorseCodePlayer()

print('Welcome to the International Morse Code Converter and Player')

convert_message = True
while convert_message:
    print("\nOptions:")
    print("1. Convert Text to Morse Code")
    print("2. Convert Morse Code to Text")
    print("3. Play Morse Code Sound")
    print("4. Exit")
    choice = input("Choose an option (1-4): ")

    if choice == '1':
        message = input("Write your message to convert to Morse Code: ")
        morse_message = international_converter.to_morse_code(message)
        print(f"Your Morse code: {morse_message}")

    elif choice == '2':
        morse_code = input("Enter Morse Code to convert to Text: ")
        text_message = international_converter.from_morse_code(morse_code)
        print(f"Your text message: {text_message}")

    elif choice == '3':
        morse_code = input("Enter Morse Code to play as sound: ")
        player.play_morse_code(morse_code)

    elif choice == '4':
        convert_message = False

    else:
        print("Invalid option, please choose a number between 1 and 4.")

print("Thank you for using the Morse Code Converter and Player!")
