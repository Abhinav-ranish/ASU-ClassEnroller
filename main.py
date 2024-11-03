import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import sys
import os
from classapi import check_class
from enrollment import login
from email_notifications import send_email
from classloader import save_class_numbers_to_json, load_class_numbers_from_json

# Configuration variables
wait_time = 1
chromedriverpath = "Driver/chromedriver"
semesternumber = '2215'
duopushid = '7'
account_sid = 'username'
auth_token = 'password'
email = os.environ.get('EMAIL')
password = os.environ.get('PASSWORD')
recipient = os.environ.get('RECIPIENT')

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
                ##send_email(class_number, 1, email, password, recipient)
                #login(driver, class_number, semesternumber, account_sid, auth_token, duopushid)
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
