
# ===========================================================
# ASU Class Enroller
# ===========================================================
# Author: Abhinav
# GitHub: https://github.com/abhinav
# Description: This script automates the process of enrolling in classes at ASU by monitoring class availability and sending notifications when a class opens up.
# ===========================================================


import json
import os

def save_class_numbers_to_json(class_numbers):
    data = {'class_numbers': class_numbers}
    with open('class_numbers.json', 'w') as file:
        json.dump(data, file)

def load_class_numbers_from_json():
    if os.path.exists('class_numbers.json'):
        with open('class_numbers.json', 'r') as file:
            data = json.load(file)
            return data.get('class_numbers', [])
    else:
        return []
