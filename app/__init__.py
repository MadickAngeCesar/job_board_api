from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials
from flask_migrate import Migrate
#from flask_mail import Mail
#from app.config import MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, MAIL_USE_TLS, MAIL_USE_SSL


db = SQLAlchemy()
migrate = Migrate()
#mail = None

def create_app():
    # Create and configure the Flask app
    app = Flask(__name__, template_folder='templates', static_folder='static')
    
    # Load configuration
    app.config.from_object('app.config.Config')

    #global mail
    #mail = Mail(app)
    
    # Initialize CORS
    CORS(app)

    # Initialize Firebase
    cred = credentials.Certificate(app.config['FIREBASE_CREDENTIALS_PATH'])
    firebase_admin.initialize_app(cred, {
        'storageBucket': app.config['FIREBASE_BUCKET_NAME']
    })

    # Initialize the database
    db.init_app(app)
    migrate.init_app(app, db)  # Initialize Flask-Migrate with app and db


    with app.app_context():
        # Create database tables
        db.create_all()

    # Import and register blueprints inside the function
    from .routes import user_bp, job_bp, application_bp, index_bp
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(job_bp, url_prefix='/jobs')
    app.register_blueprint(application_bp, url_prefix='/applications')
    app.register_blueprint(index_bp)

    return app
