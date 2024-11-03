import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from twilio.rest import Client
import yaml
import os
import json
from tinkergui import *


def save_twilio_credentials_to_yaml(account_sid, auth_token, phone_number, dest_phone_number):
    data = {
        'twilio_account_sid': account_sid,
        'twilio_auth_token': auth_token,
        'twilio_phone_number': phone_number,
        'destination_phone_number': dest_phone_number
    }
    with open('twilio_credentials.yaml', 'w') as file:
        yaml.dump(data, file)

def check_class(class_number):
    # Set up Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    service = Service('chromedriver.exe')  
    driver = webdriver.Chrome(service=service, options=chrome_options)

    time.sleep(2)
            
    url = f"https://catalog.apps.asu.edu/catalog/classes/classlist?advanced=true&campusOrOnlineSelection=C&classNbr={class_number}&honors=F&promod=F&searchType=all&term=2247"
    driver.get(url)

    time.sleep(1)

    try:
        open_seats_element = driver.find_element(By.CSS_SELECTOR, '.class-results-cell.seats .text-nowrap')
        open_seats_text = open_seats_element.text
        open_seats = int(open_seats_text.split()[0])
        return True
    except NoSuchElementException:
        print(f"Class {class_number} doesn't exist.")
        return False
    
    try:
        if open_seats > 0:
            print(f"Class {class_number} open - {open_seats} seats available")
            #send_voice_call(class_number, open_seats)
            return True
        else:
            print(f"Class {class_number} closed - No open seats.")
            return False
    except ValueError:
        print(f"Unable to determine class {class_number} status. Assuming class is closed.")
        return False

def load_twilio_credentials_from_yaml():
    with open('twilio_credentials.yaml', 'r') as file:
        data = yaml.safe_load(file)
        return (
            data['twilio_account_sid'], 
            data['twilio_auth_token'], 
            data['twilio_phone_number'], 
            data['destination_phone_number']
        )

def send_voice_call(class_number, open_seats):
    twilio_account_sid, twilio_auth_token, twilio_phone_number, destination_phone_number = load_twilio_credentials_from_yaml()
    client = Client(twilio_account_sid, twilio_auth_token)
    # Initialize Twilio client
    message = f"Class {class_number} is open and {open_seats} seats are available"
    print(message)

    # Make the call
    call = client.calls.create(
        twiml=f'<Response><Say>{message}</Say></Response>',
        to=destination_phone_number,
        from_=twilio_phone_number
    )
        
     # Print call SID for reference
    print("Call SID:", call.sid)

# Main function
def main():
    if os.path.exists('twilio_credentials.yaml'):
        print("Twilio credentials already exist. Loading from file.")
        num_classes = 0
        # num_classes = int(input("Enter the number of classes to monitor: "))


        # for _ in range(num_classes):
        #     class_number = input("Enter class number: ")
        #     class_numbers.append(class_number)

        class_info = {class_number: False for class_number in class_numbers}

        while True:
            for class_number in class_info:
                if not class_info[class_number]:
                    if check_class(class_number):
                        class_info[class_number] = True
                        #send_voice_call(class_number, 10)
                else:
                    # print(f"Class {class_number} is already open.")
                    exit()
            time.sleep(1)  # Wait for 10 minutes before checking again

        return 
    else:
        twilio_account_sid = input("Enter Twilio Account SID: ")
        twilio_auth_token = input("Enter Twilio Auth Token: ")
        twilio_phone_number = input("Enter Twilio Phone Number: ")
        destination_phone_number = input("Enter Destination Phone Number: ")  # Prompt for destination phone number
        save_twilio_credentials_to_yaml(twilio_account_sid, twilio_auth_token, twilio_phone_number, destination_phone_number)
        print("Twilio credentials saved to twilio_credentials.yaml")


if __name__ == "__main__":
    main()


