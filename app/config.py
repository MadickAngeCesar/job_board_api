import os

class Config:
    #SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    if not os.path.exists('instance'):
        os.makedirs('instance')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads/'
    #MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB limit
