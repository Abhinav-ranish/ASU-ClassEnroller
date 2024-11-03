import random
import requests

secret_numbers = {'A': 1, 'B': 34, 'C': 76, 'D': 33, 'E': 48, 'F': 44, 'G': 53, 'H': 84, 'I': 89, 'J': 73, 'K': 25, 'L': 30, 'M': 98, 'N': 26, 'O': 44, 'P': 67, 'Q': 28, 'R': 85, 'S': 12, 'T': 18, 'U': 99, 'V': 27, 'W': 22, 'X': 35, 'Y': 72, 'Z': 100, '0': 63, '1': 0, '2': 20, '3': 50, '4': 71, '5': 80, '6': 100, '7': 52, '8': 35, '9': 67}

def check_string(string):
    total = 0
    for letter in string:
        total += secret_numbers.get(letter, 0) 
    return total == 3500

def decode(output):
    original_key = output.replace("-", "")
    print(f'Original Key validity - {check_string(original_key)}')


x = input("Please Enter Liscence Key:  ")

url = "https://iron-tranquil-cosmonaut.glitch.me/secretkeyfile.txt"
response = requests.get(url)
if x == response.text:
    print("Invalid Code. Code has aldready been used.")
else:
    decode(x)
    url1 = f'https://iron-tranquil-cosmonaut.glitch.me/submit?p={x}'
    response1 = requests.get(url1)
    print("Key Successfully Used.")

    





