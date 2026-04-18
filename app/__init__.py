from flask import Flask
import os

def create_app():
    """Application factory to initialize the Incident Response system."""
    app = Flask(__name__, 
                template_folder='../templates', 
                static_folder='../static')
    
    # Register Routes
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
