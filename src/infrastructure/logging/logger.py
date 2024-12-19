import logging
from pythonjsonlogger.json import JsonFormatter

def setup_logging(app):
    handler = logging.StreamHandler()
    formatter = JsonFormatter()
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

logger = logging.getLogger(__name__)
