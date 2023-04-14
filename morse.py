
# Dictionary representing the morse code chart
#Got help from geeksforgeeks.org/morse-code/translator-python
MORSE_DICTIONARY = { 'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.', 
                    'F':'..-.', 'G':'--.', 'H':'....', 'I':'..', 'J':'.---', 
                    'K':'-.-', 'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-', '!': '-.-.--'}


def encrypt(message):
    message = message.upper()
    cipher = ''
    for character in message:
        if character != ' ':
            cipher += MORSE_DICTIONARY[character] + ' '
        else:
            cipher += ' '
    return cipher
