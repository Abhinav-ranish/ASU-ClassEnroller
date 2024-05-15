import random
import requests


Keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

secret_numbers = {'A': 1, 'B': 34, 'C': 76, 'D': 33, 'E': 48, 'F': 44, 'G': 53, 'H': 84, 'I': 89, 'J': 73, 'K': 25, 'L': 30, 'M': 98, 'N': 26, 'O': 44, 'P': 67, 'Q': 28, 'R': 85, 'S': 12, 'T': 18, 'U': 99, 'V': 27, 'W': 22, 'X': 35, 'Y': 72, 'Z': 100, '0': 63, '1': 0, '2': 20, '3': 50, '4': 71, '5': 80, '6': 100, '7': 52, '8': 35, '9': 67}

def generate_string():
    total = 0
    result = ""
    while total != 3500:
        letter = random.choice(Keys)
        total += secret_numbers[letter]
        if total > 3500:
            total -= secret_numbers[letter]
        else:
            result += letter
    while len(result) < 24:  
        result += random.choice(Keys)
    return result


def check_string(string):
    total = 0
    for letter in string:
        total += secret_numbers.get(letter, 0) 
    return total == 3500

input1 = ''
def encode():
    while True:
        input1 = generate_string()

        url = "https://iron-tranquil-cosmonaut.glitch.me/secretkeyfile.txt"

        response = requests.get(url)
        if input1 == response.text: 
            input1 = generate_string()
        else:
            length_input1 = len(input1)
            if length_input1 % 3 == 0:
                part_length = length_input1 // 3
                output = '-'.join([input1[i:i+part_length] for i in range(0, length_input1, part_length)])
                print(f'Liscence Key - {output}')
                print(f'Validity of key - {check_string(input1)}')
                return output
            else:
                print("Length of input1 is not divisible by 3. Generating a new string...")

def decode(output):
    original_key = output.replace("-", "")
    #print(f'{original_key} - 2')
    print(f'Original Key validity - {check_string(original_key)}')

x = encode()

decode(x)





