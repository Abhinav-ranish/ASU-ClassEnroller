
# ===========================================================
# ASU Class Enroller
# ===========================================================
# Author: Abhinav
# GitHub: https://github.com/abhinav
# Description: This script automates the process of enrolling in classes at ASU by monitoring class availability and sending notifications when a class opens up.
# ===========================================================


from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.common.exceptions import NoSuchElementException # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

def login(driver, class_number, semesternumber, account_sid, auth_token, duopushid, email, password, recipient):
    try:
        driver.get("https://my.asu.edu/")
        time.sleep(3)
        try:
            # Enter username and password
            driver.find_element(By.CSS_SELECTOR, '#username').send_keys(account_sid)
            driver.find_element(By.CSS_SELECTOR, '#password').send_keys(auth_token)
            driver.find_element(By.CSS_SELECTOR, 'input[name="submit"]').click()
            time.sleep(6)

            # Click on the "Other options" link again if needed
            try:
                other_options_link = driver.find_element(By.LINK_TEXT, "Other options")
                other_options_link.click()
                time.sleep(2)
            except NoSuchElementException:
                print("Other options link not found")

            # Select the authentication method in the 6th row
            try:
                driver.find_element(By.CSS_SELECTOR, f'.auth-method-wrapper:nth-child({duopushid}) .method-body-with-description').click()
                time.sleep(1)
            except NoSuchElementException:
                print(f"Authentication method in row {duopushid} not found")

            time.sleep(20)  # Wait for Duo confirmation

            # Click the "Trust this browser" button
            try:
                trust_browser_button = driver.find_element(By.ID, "trust-browser-button")
                trust_browser_button.click()
                time.sleep(7)
            except NoSuchElementException:
                print("Trust browser button not found")
        except NoSuchElementException:
            print("Aldready Logged in")

        # Adding Class

        driver.get("https://catalog.apps.asu.edu/catalog/classes")
        time.sleep(5)
        driver.find_element(By.CSS_SELECTOR, ".text-nowrap").click()
        time.sleep(2)
        driver.find_element(By.NAME, "classNbr").send_keys(class_number)
        time.sleep(2)
        driver.find_element(By.ID, "search-button").click()
        time.sleep(2)
        try:
            driver.find_element(By.CSS_SELECTOR, ".class-results-cell > .btn").click()
            time.sleep(2)
            try:
                driver.find_element(By.ID, "ASU_ADDCLAS_WRK_ADD_BTN").click()
                time.sleep(2)
                try:
                    driver.find_element(By.ID, "#ICOK").click()
                    time.sleep(1)
                except NoSuchElementException:
                    print("No confirmation needed.")
                driver.find_element(By.ID, "DERIVED_SSR_FL_SSR_ENROLL_FL").click()
                time.sleep(2)
                driver.find_element(By.ID, "#ICYes").click()
                time.sleep(1)
                print("Class enrollment completed successfully.")
                driver.quit()
            except NoSuchElementException:
                    print("Class aldready added.")    
        except:
            print("Failed adding Class..")
            sendfail_email(class_number, 1, email, password, recipient)

        # Enroll in the class
        try:
            myasu_url = "https://webapp4.asu.edu/myasu/"
            driver.get(myasu_url)
            time.sleep(5)

            driver.find_element(By.LINK_TEXT, "Registration").click()
            time.sleep(3)
            driver.find_element(By.LINK_TEXT, "Add/Shopping Cart").click()
            time.sleep(5)
            try:
                driver.find_element(By.ID, "win2divSCC_LO_FL_WRK_SCC_GROUP_BOX_1$0").click()
                time.sleep(4)
                driver.find_element(By.ID, "DERIVED_SSR_FL_SSR_CHANGE_BTN").click()
                time.sleep(2)
                driver.find_element(By.ID, "win1divACAD_CAR_TBL_DESCR$0").click()
                time.sleep(2)
            except NoSuchElementException:
                print("Term selection element not found.")
                  
            driver.find_element(By.ID, "DERIVED_SSR_FL_SSR_ENROLL_FL").click()
            time.sleep(2)
            driver.find_element(By.ID, "#ICYes").click()
            time.sleep(1)
            print("Class added successfully.")
            
        except NoSuchElementException:
            print("Class Enrollement Failed.")
    except Exception as e:
        print(f"Error during enrollment: {e}")
        sendfail_email(class_number, 1, email, password, recipient)


def sendfail_email(class_number, open_seats, email, password, recipient):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Class {class_number} is Now Open!"
    msg["From"] = email
    msg["To"] = recipient
    
    text = f"""\
    Unfortunately, we were unable to enroll you in class {class_number}.
    The class currently has at least {open_seats} open seat(s) available.
    Please manually enroll by following these steps:
    1. Go to https://my.asu.edu
    2. Click Registration -> Add/Shopping Cart -> Add by Class Number
    3. Insert {class_number} in the field and proceed to enroll.
    """

    html = f"""\
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #E74C3C;">Enrollment Failed for Class {class_number}</h2>
        <p style="font-size: 1.1em;">Unfortunately, we were unable to enroll you in the class <strong>{class_number}</strong>.</p>
        <p>The class currently has at least <strong>{open_seats} open seat(s) available</strong>.</p>
        
        <p>Please manually enroll by following these steps:</p>
        <ol>
            <li>Go to <a href="https://my.asu.edu" target="_blank">my.asu.edu</a></li>
            <li>Click <strong>Registration</strong> &rarr; <strong>Add/Shopping Cart</strong> &rarr; <strong>Add by Class Number</strong></li>
            <li>Insert <strong>{class_number}</strong> in the field and proceed to enroll</li>
        </ol>
        
        <footer style="margin-top: 20px; color: #777;">
            <p>Best of luck,</p>
            <a href="https://github.com/Abhinav-ranish"> Your Enrollment Automation Script</a>
        </footer>
    </body>
    </html>
    """
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    msg.attach(part1)
    msg.attach(part2)

    server.sendmail(email, recipient, msg.as_string())
    server.quit()
    print("HTML email with manual enrollment instructions sent successfully.")
