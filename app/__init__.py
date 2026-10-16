"""Application factory for the 'Wie würdest du urteilen?' project."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # Import models before create_all so SQLAlchemy knows every table.
    from app import models  # noqa: F401
    with app.app_context():
        db.create_all()
        from app.cases.case_loader import sync_cases_to_database
        sync_cases_to_database()

    return app
