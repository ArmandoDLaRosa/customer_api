from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from infrastructure.config import settings
from infrastructure.container import Container
from infrastructure.logging.logger import setup_logging
from infrastructure.metrics import setup_metrics
from interfaces.http.auth import bp as auth_bp
from interfaces.http.errors import errors
from interfaces.http.v1.docs.api_docs import register_api_docs
from interfaces.http.v1.routes.customers import bp as customers_bp


def create_app():

    app = Flask(__name__)
    
    # Configuration
    app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY
    app.config['LOG_LEVEL'] = "INFO"
    
    # Logging
    setup_logging(app)
    app.logger.info("Application startup: Configured logging.")

    # Metrics
    setup_metrics(app)
    app.logger.info("Metrics setup complete.")

    # Dependency Injection
    container = Container()
    container.init_resources()
    container.config.from_dict(settings)

    # Flask Extensions
    JWTManager(app)
    CORS(app, resources={r"/v1/*": {"origins": "*"}})

    # API Documentation
    register_api_docs(app)

    # Register Routes
    app.register_blueprint(customers_bp, url_prefix='/v1/customers')
    app.register_blueprint(auth_bp, url_prefix='/v1/auth')
    app.register_blueprint(errors)

    # Healthcheck
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"}), 200

    # Metrics Endpoint
    @app.route('/metrics')
    def metrics_endpoint():
        return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
