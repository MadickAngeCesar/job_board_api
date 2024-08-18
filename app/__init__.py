from app.routes import bp as api_bp
from config import Config
from models import db

def create_app():
    
    with Config.app.app_context():
        db.create_all()

    Config.app.register_blueprint(api_bp, url_prefix='/api')

    return Config.app