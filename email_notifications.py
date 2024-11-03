import smtplib
from email.mime.text import MIMEText

def send_email(class_number, open_seats, email, password, recipient):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    message = f"Subject: Class {class_number} Open\n\nClass {class_number} is open with {open_seats} seats. Enrolling now."
    server.sendmail(email, recipient, message)
    server.quit()
    print("Email sent successfully.")
