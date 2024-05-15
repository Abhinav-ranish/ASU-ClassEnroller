import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from twilio.rest import Client
import yaml
import os
import webbrowser
import json

#to install pyinstaller --onefile --icon="my_icon.ico" my_script.py

class_info = {}

def save_twilio_credentials_to_yaml(account_sid, auth_token, phone_number, dest_phone_number, wtime):
    data = {
        'twilio_account_sid': account_sid,
        'twilio_auth_token': auth_token,
        'twilio_phone_number': phone_number,
        'destination_phone_number': dest_phone_number,
        'wait_time' : wtime
    }
    with open('twilio_credentials.yaml', 'w') as file:
        yaml.dump(data, file)

def check_class(class_number):
    #selenium
    chrome_options = Options()
    #chrome_options.add_argument("--headless")  
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
        #time.sleep(10)
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


#Failed Test using img
    # imgs = driver.find_elements(By.CSS_SELECTOR, 'cl[iconName]')
    # for img in imgs:
    #     data_icon = img.get_attribute('iconName')
    #     if data_icon == 'xmark':
    #         print("Class closed")
    #         #driver.quit()
    #         return False  
    #     elif data_icon == 'circle':
    #         print("Class open")
    #         driver.quit()
    #         return True  
    #driver.quit()
    
#Example Case
    #class_number = '60459'  # Replace '12345' with the actual class number
    # class_status = check_class(class_number)
    # if class_status is not None:
    #     print(f"Class {class_number} is {'open' if class_status else 'closed'}.")
    # else:
    #     print(f"Class {class_number} status is not available.")

# Function to send Discord webhook

def load_twilio_credentials_from_yaml():
    with open('twilio_credentials.yaml', 'r') as file:
        data = yaml.safe_load(file)
        return (
            data['twilio_account_sid'], 
            data['twilio_auth_token'], 
            data['twilio_phone_number'], 
            data['destination_phone_number'],
            data['wait_time']
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

# Main function
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

        if os.path.exists('twilio_credentials.yaml'):
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\nTwilio credentials already exist. Loading from file.\nTo make changes find Twillo file")
            
            num_classes = int(input("Enter the number of classes to monitor: "))

            waittime = int(1200)
            wait_time_minutes = load_twilio_credentials_from_yaml()[4]
            waittime = int(wait_time_minutes) * 60
            #print("\nDont spam ASU servers. You most likely will get IP banned.\nSuggest you to use 10 mins")
            #waittime = int(input("Wait time per round (minutes): "))*60
            
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
                            #send_voice_call(class_number, 10)
                        else:
                            print("Waiting for class to open... Will ping you when open.")
                    else:
                        print(f"Class {class_number} is already open.")
                        at_least_one_class_opened = True
                
                if at_least_one_class_opened:
                    break  # Exit the loop if at least one class opens
                
                print(f'No classes opened yet. Checking again in {wait_time_minutes} minutes.')
                time.sleep(waittime)  # Wait for 1 second before checking again

            return 
        else:
            choice = input("Open Login Page for Twillio (yes - y)")
            if choice.lower() == 'y' or choice.lower() == 'yes':    
                webbrowser.open("https://www.twilio.com/login")
            print("If you dont want a phone call you can skip this process by just pressing Enter.\n")
            twilio_account_sid = input("Enter Twilio Account SID: ")
            twilio_auth_token = input("Enter Twilio Auth Token: ")
            twilio_phone_number = input("Enter Twilio Phone Number: ")
            destination_phone_number = input("Enter Your Phone Number: ")  # Prompt for destination phone number
            wait_time = input("\nEnter wait time betwewen web scrape: ")
            save_twilio_credentials_to_yaml(twilio_account_sid, twilio_auth_token, twilio_phone_number, destination_phone_number, wait_time)
            print("Twilio credentials saved to twilio_credentials.yaml\n")
            time.sleep(1)

if __name__ == "__main__":
    main()


