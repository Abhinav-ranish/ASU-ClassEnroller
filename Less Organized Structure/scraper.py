import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import json
import sys

#pyinstaller --onefile --icon="my_icon.ico" my_script.py

# Stuff to be edited ( FOR SCRAPING )
wait_time = 1
chromedriverpath = "/Users/abhinav/Documents/Github/ASU-ClassEnroller/chromedriver"

# Stuff to be edited ( FOR ENROLLING )
semesternumber = '2215' # 2215 for Spring 2025
duopushid = '7' # Which Duo Push option to select ( Starting from 1 - How many options you have which one would you like to select)


# Initialize the Chrome driver 
chrome_options = Options()
chrome_options.add_argument("--disable-site-isolation-trials")
service = Service(chromedriverpath) 
driver = webdriver.Chrome(service=service, options=chrome_options) 

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '-y':
        previous_class_numbers = load_class_numbers_from_json()
        class_numbers = previous_class_numbers if previous_class_numbers else []
    else:
        class_numbers = []

    if not class_numbers:
        num_classes = int(input("Enter the number of classes to monitor: "))
        for _ in range(num_classes):
            class_number = input("Enter class number: ")
            class_numbers.append(class_number)
        save_class_numbers_to_json(class_numbers)

    class_info = {number: False for number in class_numbers}  # Initialize each class as "closed"
    waittime = wait_time * 60 if wait_time != 0 else 1200

    while True:
        at_least_one_class_opened = False

        for class_number in class_numbers:
            if not class_info[class_number]:  # Only check if class hasn't been marked as "open"
                if check_class(class_number):
                    class_info[class_number] = True
                    at_least_one_class_opened = True
                    with open('file.txt', 'w') as file:
                        file.write(class_number)
                    # ENABLE THESE IF YOU WANT TO SEND EMAILS OR AUTOENROLL
                    #send_email(class_number, open_seats)
                    #print(f"\n\nClass {class_number} opened. Enrolling now...")
                    #login(class_number)

                else:
                    print(f"Waiting for class {class_number} to open... Will notify when open.")
            else:
                print(f"Class {class_number} is already open.")

        if at_least_one_class_opened:
            break

        print(f'No classes opened yet. Checking again in {wait_time} minutes.')
        time.sleep(waittime)
        driver.refresh()

    driver.quit()

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

def check_class(class_number):
    try:
        # Navigate to the ASU catalog classes page
        driver.get("https://catalog.apps.asu.edu/catalog/classes")
        time.sleep(1)

        # Dismiss the cookie consent banner if it appears
        try:
            cookie_accept_button = driver.find_element(By.ID, "rcc-confirm-button")
            cookie_accept_button.click()
            time.sleep(1)
        except NoSuchElementException:
            print("Cookie consent banner not found or already dismissed")

        # Click on the "Advanced Search" link
        advanced_search_link = driver.find_element(By.CSS_SELECTOR, ".text-nowrap")
        advanced_search_link.click()
        time.sleep(1)

        # Enter the class number
        class_number_field = driver.find_element(By.NAME, "classNbr")
        class_number_field.clear()
        class_number_field.send_keys(class_number)
        time.sleep(1)

        # Click on the search button
        search_button = driver.find_element(By.ID, "search-button")
        search_button.click()
        time.sleep(3)  # Wait for the search results to load

        # Check for open seats
        try:
            open_seats_element = driver.find_element(By.CSS_SELECTOR, '.class-results-cell.seats .text-nowrap')
            open_seats_text = open_seats_element.text
            open_seats = int(open_seats_text.split()[0])
            print(f"{open_seats} seats available for class {class_number}")
            if open_seats > 0:
                print(f"Class {class_number} open - {open_seats} seats available")
                return True
            else:
                print(f"Class {class_number} closed - No open seats.")
                return False
        except NoSuchElementException:
            print(f"Class {class_number} doesn't exist.")
            return False
    except ValueError:
        print(f"Unable to determine class {class_number} status. Assuming class is closed.")
        return False

def send_email(class_number, open_seats):
    # Send email notification
    email = os.environ.get('EMAIL')
    password = os.environ.get('PASSWORD')
    recipient = os.environ.get('RECIPIENT')

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    message = f"Subject: Class {class_number} Open\n\nClass {class_number} is open and {open_seats} seats are available. Trying to Enroll Dont Forget to add your new onetime code."
    server.sendmail(email, recipient, message)
    server.quit()
    print(message)
    print("Email sent successfully.")
    pass

def login(class_number):
    try:
        account_sid = 'username'   # ASU username
        auth_token = 'password'    # ASU password
        url = "https://my.asu.edu/"
        driver.get(url)
        
        time.sleep(3)

        # Entering username and password
        username_field = driver.find_element(By.CSS_SELECTOR, '#username')
        password_field = driver.find_element(By.CSS_SELECTOR, '#password')
        login_button = driver.find_element(By.CSS_SELECTOR, 'input[name="submit"]')

        username_field.send_keys(account_sid)
        password_field.send_keys(auth_token)
        login_button.click()

        time.sleep(5)

        # Switch to Duo frame and click on "Other options"
        driver.switch_to.frame(0)
        other_options_button = driver.find_element(By.CSS_SELECTOR, '.button--link')
        other_options_button.click()

        time.sleep(2)

        # Select "Duo Push" for authentication
        duo_push_option = driver.find_element(By.CSS_SELECTOR, f'.auth-method-wrapper:nth-child({duopushid}) .method-body-with-description')
        duo_push_option.click()

        time.sleep(20) # Wait for the call to be accepted

        # Navigate to the specific ASU class registration page
        url1 = f"https://www.asu.edu/go/addclass/?STRM={semesternumber}&ASU_CLASS_NBR={class_number}"
        driver.get(url1)
        time.sleep(5)

        # Attempt to add the class
        try:
            add_class_button = driver.find_element(By.ID, "ASU_ADDCLAS_WRK_ADD_BTN")
            add_class_button.click()

            time.sleep(5)

            # Confirm enrollment
            enroll_button = driver.find_element(By.ID, "DERIVED_SSR_FL_SSR_ENROLL_FL")
            enroll_button.click()

            time.sleep(2)
            
            # Confirm enrollment if prompted
            driver.find_element(By.ID, "#ICYes").click()
            print("Class added successfully. Exiting browser.")
        except Exception as e:
            print(f"Error occurred: {e}. Retrying enrollment.")
            url2= 'https://cs.oasis.asu.edu/psc/asucsprd_13/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_MD_SP_FL.GBL?Action=U&MD=Y&GMenu=SSR_STUDENT_FL&GComp=SSR_START_PAGE_FL&GPage=SSR_START_PAGE_FL&scname=CS_SSR_MANAGE_CLASSES_NAV'
            driver.get(url2)
            time.sleep(5)

            # Confirm enrollment
            enroll_button = driver.find_element(By.ID, "DERIVED_SSR_FL_SSR_ENROLL_FL")
            enroll_button.click()

            time.sleep(2)
            
            # Confirm enrollment if prompted
            driver.find_element(By.ID, "#ICYes").click()
            print("Class added successfully after retry. Exiting browser.")

        print("Class added successfully. Exiting browser.")
        time.sleep(5)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()

# THIS IS FOR THE VOICE CALL FUNCTIONALITY

# twilio_account_sid = None
# twilio_auth_token = None
# twilio_phone_number = None
# destination_phone_number = None

# from twilio.rest import Client
# def send_voice_call(class_number, open_seats):
#     client = Client(twilio_account_sid, twilio_auth_token)
#     message = f"Class {class_number} is open and {open_seats} seats are available"
#     print(message)

#     # Make the call
#     call = client.calls.create(
#         twiml=f'<Response><Say>{message}</Say></Response>',
#         to=destination_phone_number,
#         from_=twilio_phone_number
#     )
        
#      # Print call SID for reference
#     print("Call SID:", call.sid)

