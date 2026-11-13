import os
 
 
class Config:
    """Application configuration loaded from environment variables."""
 
    APP_NAME = os.getenv("APP_NAME", "DevOps Deployment Monitor")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "Development")
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() in ("true", "1", "yes")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "5000"))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
