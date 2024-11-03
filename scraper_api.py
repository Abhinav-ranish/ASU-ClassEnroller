
# ===========================================================
# ASU Class Enroller
# ===========================================================
# Author: Abhinav
# GitHub: https://github.com/abhinav
# Description: This script automates the process of enrolling in classes at ASU by monitoring class availability and sending notifications when a class opens up.
# ===========================================================

import time
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.common.exceptions import NoSuchElementException # type: ignore

def check_class(driver, class_number):
    try:
        driver.get("https://catalog.apps.asu.edu/catalog/classes")
        time.sleep(1)

        # Dismiss the cookie consent banner
        try:
            cookie_accept_button = driver.find_element(By.ID, "rcc-confirm-button")
            cookie_accept_button.click()
            time.sleep(1)
        except NoSuchElementException:
            print("Cookie consent banner not found or already dismissed")

        # Advanced Search link and class number input
        advanced_search_link = driver.find_element(By.CSS_SELECTOR, ".text-nowrap")
        advanced_search_link.click()
        time.sleep(1)

        class_number_field = driver.find_element(By.NAME, "classNbr")
        class_number_field.clear()
        class_number_field.send_keys(class_number)
        time.sleep(1)

        # Search and check for open seats
        search_button = driver.find_element(By.ID, "search-button")
        search_button.click()
        time.sleep(3)

        open_seats_element = driver.find_element(By.CSS_SELECTOR, '.class-results-cell.seats .text-nowrap')
        open_seats_text = open_seats_element.text
        open_seats = int(open_seats_text.split()[0])
        print(f"{open_seats} seats available for class {class_number}")
        
        return open_seats > 0
    except (NoSuchElementException, ValueError):
        print(f"Error determining status for class {class_number}. Assuming class is closed.")
        return False
