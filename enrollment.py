from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def login(driver, class_number, semesternumber, account_sid, auth_token, duopushid):
    try:
        driver.get("https://my.asu.edu/")
        time.sleep(3)

        # Enter username and password
        driver.find_element(By.CSS_SELECTOR, '#username').send_keys(account_sid)
        driver.find_element(By.CSS_SELECTOR, '#password').send_keys(auth_token)
        driver.find_element(By.CSS_SELECTOR, 'input[name="submit"]').click()
        time.sleep(5)

        # Duo Authentication
        driver.switch_to.frame(0)
        driver.find_element(By.CSS_SELECTOR, '.button--link').click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, f'.auth-method-wrapper:nth-child({duopushid}) .method-body-with-description').click()
        time.sleep(20)  # Wait for Duo confirmation

        # Enroll in the class
        enroll_url = f"https://www.asu.edu/go/addclass/?STRM={semesternumber}&ASU_CLASS_NBR={class_number}"
        driver.get(enroll_url)
        time.sleep(5)

        driver.find_element(By.ID, "ASU_ADDCLAS_WRK_ADD_BTN").click()
        time.sleep(5)
        driver.find_element(By.ID, "DERIVED_SSR_FL_SSR_ENROLL_FL").click()
        time.sleep(2)
        driver.find_element(By.ID, "#ICYes").click()
        print("Class added successfully.")
    except Exception as e:
        print(f"Error during enrollment: {e}")
    finally:
        driver.quit()
