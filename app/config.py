import os

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
