#!/usr/bin/env python3

#   format_morse_code

def format_morse_code(decoded_message):
    # Convert the to lowercase
    lower_case_message = decoded_message.lower()

    # Replace spaces with underscores
    formatted_message = lower_case_message.replace(' ', '_')

    # Wrap the formatted message with picoCTF{}
    flag = f"picoCTF{{{formatted_message}}}"

    return flag
# The decoded Morse code message 
decoded_message = "WH47 H47H 90D W20U9H7"

# Get the formatted flag
formatted_flag = format_morse_code(decoded_message)

# Print the results
print(formatted_flag)
