from datetime import datetime, timezone
import socket
 
from flask import current_app, jsonify, render_template_string
 
 
def register_routes(app):
    """Register the application's HTTP endpoints."""
 
    @app.get("/")
    def home():
        return render_template_string(
            """<!DOCTYPE html>
<html>
<head>
    <title>{{ app_name }}</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f6f9; text-align: center; padding: 50px; }
        .container { background: white; padding: 30px; border-radius: 10px; max-width: 650px; margin: auto; }
        h1 { color: #1f4e79; }
        .status { color: green; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ app_name }}</h1>
        <h2 class="status">Application is Running</h2>
        <p><strong>Version:</strong> {{ version }}</p>
        <p><strong>Environment:</strong> {{ environment }}</p>
        <p><strong>Server:</strong> {{ hostname }}</p>
        <hr>
        <p>Deployed using Docker and Jenkins CI/CD</p>
    </div>
</body>
</html>""",
            app_name=current_app.config["APP_NAME"],
            version=current_app.config["APP_VERSION"],
            environment=current_app.config["ENVIRONMENT"],
            hostname=socket.gethostname(),
        )
 
    @app.get("/health")
    def health():
        return jsonify({
            "status": "healthy",
            "application": current_app.config["APP_NAME"],
            "version": current_app.config["APP_VERSION"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }), 200
 
    @app.get("/version")
    def version():
        return jsonify({
            "application": current_app.config["APP_NAME"],
            "version": current_app.config["APP_VERSION"],
            "environment": current_app.config["ENVIRONMENT"],
        }), 200
 
    @app.get("/deployment")
    def deployment():
        return jsonify({
            "status": "deployed",
            "environment": current_app.config["ENVIRONMENT"],
            "hostname": socket.gethostname(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }), 200
