import os
import smtplib

"""smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'your-email@gmail.com'
smtp_pass = 'your-email-password'

try:
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        print("SMTP connection successful!")
except Exception as e:
    print(f"SMTP connection failed: {e}")"""

class Config:
    # General configurations
    #SECRET_KEY = os.environ.get('SECRET_KEY', 'your_default_secret_key')
    
    # Database configurations
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Firebase configurations
    FIREBASE_CREDENTIALS_PATH = 'app/utils/jobboardapi-firebase-adminsdk.json'
    FIREBASE_BUCKET_NAME = 'jobboardapi.appspot.com'
    
    # CORS settings
    #CORS_HEADERS = 'Content-Type'
