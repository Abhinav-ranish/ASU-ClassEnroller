
# ===========================================================
# ASU Class Enroller
# ===========================================================
# Author: Abhinav
# GitHub: https://github.com/abhinav
# Description: This script automates the process of enrolling in classes at ASU by monitoring class availability and sending notifications when a class opens up.
# ===========================================================

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import sys
import os
from scraper_api import check_class
from enrollment import login
from email_notifications import send_email
from backup import save_class_numbers_to_json, load_class_numbers_from_json

# Enroller is still super glitchy. If your are checking for more than one class I would avoiding using that till the next update.
# Configuration variables
wait_time = 1
chromedriverpath = "Driver/chromedriver" # GET RELATIVE PATH OF CHROME DRIVER BASED ON YOUR PC (windows add ----.exe) (arm mac use armchromedriver)
semesternumber = '2215'
duopushid = '3' # Use the phone call id on duo push.
account_sid = '' # ASURITE
auth_token = '' # ASU PASSWORD
# SMTP SETUP
email = '@gmail.com' # Personal EMAIL
password = 'supersecretapppassword' # APP PASSWORD (google account settigns-> App Password)
recipient = 'presidentofjoy@asu.edu'

# Initialize Chrome driver
chrome_options = Options()
chrome_options.add_argument("--disable-site-isolation-trials")
service = Service(chromedriverpath)
driver = webdriver.Chrome(service=service, options=chrome_options)

def main():
    previous_class_numbers = load_class_numbers_from_json() if '-y' in sys.argv else []
    class_numbers = previous_class_numbers if previous_class_numbers else []

    if not class_numbers:
        num_classes = int(input("Enter the number of classes to monitor: "))
        for _ in range(num_classes):
            class_number = input("Enter class number: ")
            class_numbers.append(class_number)
        save_class_numbers_to_json(class_numbers)

    class_info = {number: False for number in class_numbers}
    waittime = wait_time * 60 if wait_time != 0 else 1200

    while True:
        at_least_one_class_opened = False

        for class_number in class_numbers:
            if not class_info[class_number] and check_class(driver, class_number):
                class_info[class_number] = True
                at_least_one_class_opened = True
                send_email(class_number, 1, email, password, recipient)
                #login(driver, class_number, semesternumber, account_sid, auth_token, duopushid, email, password, recipient)
            else:
                print(f"Waiting for class {class_number} to open...")

        if at_least_one_class_opened:
            break

        print(f'No classes opened yet. Checking again in {wait_time} minutes.')
        time.sleep(waittime)
        driver.refresh()

    driver.quit()

if __name__ == "__main__":
    main()
