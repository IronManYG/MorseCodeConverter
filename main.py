from converter import MorseCodeConverter
from morse_code_player import MorseCodePlayer
from morse_code_data import international_code  # Import the dictionary


def get_user_choice():
    while True:
        choice = input("Choose an option (1-4): ")
        if choice in ['1', '2', '3', '4']:
            return choice
        else:
            print("Invalid option, please choose a number between 1 and 4.")


def get_yes_or_no(prompt):
    while True:
        response = input(prompt).lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please answer with 'yes' or 'no'.")


international_converter = MorseCodeConverter(international_code)
player = MorseCodePlayer()

print('Welcome to the International Morse Code Converter and Player')

convert_message = True
while convert_message:
    print("\nOptions:")
    print("1. Convert Text to Morse Code and Optionally Play Sound")
    print("2. Convert Morse Code to Text and Optionally Play Sound")
    print("3. Play Morse Code Sound")
    print("4. Exit")
    choice = get_user_choice()

    if choice == '1':
        message = input("Write your message to convert to Morse Code: ")
        morse_message = international_converter.to_morse_code(message)
        print(f"Your Morse code: {morse_message}")

        if get_yes_or_no("Do you want to play the Morse code sound? (Yes/No): "):
            player.play_morse_code(morse_message)
            print("Sound playback finished.")

    elif choice == '2':
        morse_code = input("Enter Morse Code to convert to Text: ")
        text_message = international_converter.from_morse_code(morse_code)
        print(f"Your text message: {text_message}")

        if get_yes_or_no("Do you want to play the Morse code sound? (Yes/No): "):
            player.play_morse_code(morse_code)
            print("Sound playback finished.")

    elif choice == '3':
        morse_code = input("Enter Morse Code to play as sound: ")
        player.play_morse_code(morse_code)
        print("Sound playback finished.")

    elif choice == '4':
        convert_message = False

print("Thank you for using the Morse Code Converter and Player!")
