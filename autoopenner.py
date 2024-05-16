import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
# from twilio.rest import Client
import os



def load_class_number():
    with open('file.txt', 'r') as file:
        class_number = file.read()
        return class_number
    
def login():
    chrome_options = Options()
    chrome_options.add_argument("--disable-site-isolation-trials")
    service = Service('chromedriver.exe')  
    driver = webdriver.Chrome(service=service, options=chrome_options) 
    try:
        class_number = load_class_number()
        account_sid = 'username'   # ASU username
        auth_token = 'password'
        duo_push = '123456' #change this to wtv
        url = f"https://my.asu.edu/"
        driver.get(url)
        
        time.sleep(3)

        username_field = driver.find_element(By.CSS_SELECTOR, '#username')
        password_field = driver.find_element(By.CSS_SELECTOR, '#password')
        login_button = driver.find_element(By.CSS_SELECTOR, 'input[name="submit"]')

        username_field.send_keys(account_sid)
        password_field.send_keys(auth_token)
        login_button.click()

        time.sleep(5)

        driver.switch_to.frame(0)

        duo_passcode = driver.find_element(By.ID, "passcode")
        duo_passcode.click()


        duo_textfield = driver.find_element(By.NAME, "passcode")
        duo_textfield.send_keys(duo_push)

        passcode_submit_button = driver.find_element(By.ID, "passcode")
        passcode_submit_button.click()

        time.sleep(5)

        url1 = f"https://www.asu.edu/go/addclass/?STRM=2247&ASU_CLASS_NBR={class_number}"

        driver.get(url1)

        time.sleep(5)

        addclass = driver.find_element(By.ID, "ASU_ADDCLAS_WRK_ADD_BTN")
        addclass.click()

        time.sleep(5)

        enroll = driver.find_element(By.ID, "DERIVED_SSR_FL_SSR_ENROLL_FL")
        enroll.click()

        time.sleep(2)

        
        driver.find_element(By.ID, "#ICYes").click()

        print("Class added successfully. Exiting browser.")


        time.sleep(5)
    finally:
        driver.quit()


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
