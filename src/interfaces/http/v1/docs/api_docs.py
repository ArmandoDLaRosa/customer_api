import os
from flasgger import Swagger

def register_api_docs(app):
    app.config["SWAGGER"] = {
        "title": "Customer Management API",
        "uiversion": 3,
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Enter your JWT token as: Bearer <token>"
            }
        },
        "security": [{"Bearer": []}]
    }
    Swagger(app)