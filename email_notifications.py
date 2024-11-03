
# ===========================================================
# ASU Class Enroller
# ===========================================================
# Author: Abhinav
# GitHub: https://github.com/abhinav
# Description: This script automates the process of enrolling in classes at ASU by monitoring class availability and sending notifications when a class opens up.
# ===========================================================


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def send_email(class_number, open_seats, email, password, recipient):
    # Set up the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    
    # Create the email headers and subject
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Class {class_number} is Now Open!"
    msg["From"] = email
    msg["To"] = recipient

    # Text version (plain text as a fallback)
    text = f"""\
    Class {class_number} is now open with atleast {open_seats} open seat available.
    We are attempting to enroll you now.

    If the auto-enroller fails, you can manually enroll:
    1. Go to https://my.asu.edu
    2. Click Registration -> Add/Shopping Cart -> Add by Class Number
    3. Insert {class_number} in the field.
    """

    # HTML version (formatted version)
    html = f"""\
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #2E86C1;">Class {class_number} is Now Open!</h2>
        <p style="font-size: 1.1em;">Good news! The class <strong>{class_number}</strong> currently has atleast <strong>{open_seats} open seat available</strong>.</p>
        <p>We are attempting to enroll you now.</p>
        
        <p>If the auto-enroller does not work, you can manually enroll by following these steps:</p>
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

    # Attach both plain text and HTML to the email
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    msg.attach(part1)
    msg.attach(part2)

    # Send the email
    server.sendmail(email, recipient, msg.as_string())
    server.quit()
    print("HTML email with manual enrollment instructions sent successfully.")
