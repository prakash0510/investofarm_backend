import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from pathlib import Path
import random
from jinja2 import Template

BASE_DIR = Path(__file__).resolve().parent.parent  
TEMPLATE_DIR = BASE_DIR / "templates"

def add_otp(file_path, otp):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            template_content = file.read()

        # Use Jinja2 to render the template
        template = Template(template_content)
        updated_content = template.render(otp=otp)

        return updated_content
    except Exception as e:
        print(f"Error: {e}\nFile Path: {file_path}")
        return None

def read_html_template(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print(f"Error: {e}\n {file_path}")

async def sent_otp_email(email,trmplate=None):
    otp = random.randint(100000, 999999)
    smtp_server = "smtp.gmail.com"  
    smtp_port = 587  
    sender_email = "noreplyinvestofarms@gmail.com"
    receiver_email = email
    sender_password = "vhwh irea unwn vgia" 

    html_template_path = TEMPLATE_DIR / "email_template.html"
    updated_content = add_otp(html_template_path, otp)

    if not updated_content:
        return "Failed to update the template with OTP."

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Your OTP for Verification"

    msg.attach(MIMEText(updated_content, "html"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  
            server.login(sender_email, sender_password)  
            server.sendmail(sender_email, receiver_email, msg.as_string())  
        return {"data":"Email sent successfully!"}
    except Exception as e:
        return f"Error: {e}"
    
    