from flask import Flask
from prometheus_client import Summary, Counter

REQUEST_COUNT = Counter('request_count', 'Number of requests received')
REQUEST_LATENCY = Summary('request_latency_seconds', 'Request latency')

def setup_metrics(app: Flask):
    @app.before_request
    def before_request():
        REQUEST_COUNT.inc()
