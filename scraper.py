import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from twilio.rest import Client
import os
import json

#to install pyinstaller --onefile --icon="my_icon.ico" my_script.py

class_info = {}

twilio_account_sid = None
twilio_auth_token = None
twilio_phone_number = None
destination_phone_number = None
wait_time = None


def check_class(class_number):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=10,10")
    chrome_options.add_argument("--disable-site-isolation-trials")
    service = Service('chromedriver.exe') 
    driver = webdriver.Chrome(service=service, options=chrome_options) 
    driver.set_window_position(2000, 0)  
    try:
        url = f"https://catalog.apps.asu.edu/catalog/classes/classlist?advanced=true&campusOrOnlineSelection=C&classNbr={class_number}&honors=F&promod=F&searchType=all&term=2247"
        driver.get(url)
        
        time.sleep(5)    

        open_seats_element = driver.find_element(By.CSS_SELECTOR, '.class-results-cell.seats .text-nowrap')
        open_seats_text = open_seats_element.text
        open_seats = int(open_seats_text.split()[0])
        print(f"{open_seats} seats available")
        if open_seats > 0:
            print(f"Class {class_number} open - {open_seats} seats available")
            #send_voice_call(class_number, open_seats)
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




def send_voice_call(class_number, open_seats):
    client = Client(twilio_account_sid, twilio_auth_token)
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

class_info = {}

def save_class_numbers_to_json(class_numbers):
    data = {
        'class_numbers': class_numbers
    }
    with open('class_numbers.json', 'w') as file:
        json.dump(data, file)

def load_class_numbers_from_json():
    if os.path.exists('class_numbers.json'):
        with open('class_numbers.json', 'r') as file:
            data = json.load(file)
            return data.get('class_numbers', [])
    else:
        return []

def main():
    while True:
        previous_class_numbers = load_class_numbers_from_json()
        if previous_class_numbers:
            choice1 = input("Previous class numbers found. Do you want to reload them? (yes/no): ")
            if choice1.lower() == 'yes':
                class_numbers = previous_class_numbers
            else:
                class_numbers = []
        else:
            class_numbers = []

       # num_classes = int(input("Enter the number of classes to monitor: ")) # only making 1 class for now
        num_classes = int(1)
        
        if wait_time == 0:
            waittime = int(1200)
        else:
            wait_time_minutes = wait_time
            waittime = int(wait_time_minutes) * 60
        
            
        for _ in range(num_classes - len(class_numbers)):
            class_number = input("Enter class number: ")
            class_numbers.append(class_number)
            class_info[class_number] = False
        save_class_numbers_to_json(class_numbers)


        while True:
            at_least_one_class_opened = False
                
            for class_number in class_numbers:
                if class_number not in class_info or not class_info[class_number]:
                    if check_class(class_number):
                        class_info[class_number] = True
                        at_least_one_class_opened = True
                        with open('file.txt', 'w') as file:
                            file.write(class_number)
                        os.system('cls' if os.name == 'nt' else 'clear')
                        os.system('python autoopenner.py')
                    else:
                        print("Waiting for class to open... Will ping you when open.")
                else:
                    print(f"Class {class_number} is already open.")
                
            if at_least_one_class_opened:
                break  
                
            print(f'No classes opened yet. Checking again in {wait_time_minutes} minutes.')
            time.sleep(waittime)  

        return 


if __name__ == "__main__":
    main()


