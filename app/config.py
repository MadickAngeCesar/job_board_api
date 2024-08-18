from app.models import db
from firebase_admin import credentials, initialize_app
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask import Flask

class Config:
    # Initialize JWTManager
    jwt = JWTManager()

    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Replace with your database URI
    db.init_app(app)
    jwt.init_app(app)

    cred = credentials.Certificate("app/jobboardapi-firebase-adminsdk.json")
    initialize_app(cred, {'storageBucket': 'jobboardapi.appspot.com'})
