import logging
from flask import Flask
from app.config import Config
 
 
def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)
 
    logging.basicConfig(
        level=getattr(logging, app.config["LOG_LEVEL"].upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
 
    from app.routes import register_routes
    register_routes(app)
 
    app.logger.info("Application initialized successfully")
    return app
