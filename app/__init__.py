from app.routes import bp as api_bp
from app.config import Config
from app.models import db

def create_app():
    
    with Config.app.app_context():
        db.create_all()

    Config.app.register_blueprint(api_bp, url_prefix='/api')

    return Config.app