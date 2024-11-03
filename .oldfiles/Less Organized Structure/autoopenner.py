import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os

chromedriverpath = "/chromedriver"
# 2215 for Spring 2025
 # Which Duo Push option to select ( Starting from 1 - How many options you have which one would you like to select)

def load_class_number():
    with open('file.txt', 'r') as file:
        class_number = file.read()
        return class_number




def main():
    while True:
        if os.path.exists('file.txt'):
            print("\nClass number already exists. Loading from file.\n")
            login()
            return
        else:
            print("\nClass number does not exist.\n")
            return

if __name__ == "__main__":
    main()
