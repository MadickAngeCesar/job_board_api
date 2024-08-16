from flask import Flask
from app.config import Config
from app.models import db
from app.routes import setup_routes



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    setup_routes(app)

    with app.app_context():
        db.create_all()

    return app
