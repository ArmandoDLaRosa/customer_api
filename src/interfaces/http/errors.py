import uuid

from application.exceptions import ApplicationException
from domain.exceptions import DomainException
from flask import Blueprint, jsonify
from infrastructure.logging.logger import logger
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest, NotFound, UnprocessableEntity

errors = Blueprint("errors", __name__)

def generate_error_id():
    return str(uuid.uuid4())

def format_error(message, code, error_id=None, details=None):
    error_response = {"error": {"message": message, "code": code}}
    if error_id:
        error_response["error"]["error_id"] = error_id
    if details:
        error_response["error"]["details"] = details
    return jsonify(error_response)

def log_error(e, level="error", error_id=None):
    log_func = getattr(logger, level, logger.error)
    log_message = f"Error: {e}"
    if error_id:
        log_message += f" | Error ID: {error_id}"
    log_func(log_message, exc_info=True)

@errors.app_errorhandler(DomainException)
def handle_domain_exception(e):
    error_id = generate_error_id()
    log_error(e, level="warning", error_id=error_id)
    return format_error(str(e), "DOMAIN_ERROR", error_id=error_id), 400

@errors.app_errorhandler(ApplicationException)
def handle_application_exception(e):
    error_id = generate_error_id()
    log_error(e, level="error", error_id=error_id)
    return format_error(str(e), "APPLICATION_ERROR", error_id=error_id), 500

@errors.app_errorhandler(NotFound)
def handle_not_found(e):
    error_id = generate_error_id()
    log_error(e, level="warning", error_id=error_id)
    return format_error("Resource not found", "NOT_FOUND", error_id=error_id), 404

@errors.app_errorhandler(BadRequest)
def handle_bad_request(e):
    error_id = generate_error_id()
    log_error(e, level="warning", error_id=error_id)
    return format_error("Bad request", "BAD_REQUEST", error_id=error_id), 400

@errors.app_errorhandler(ValidationError)
def handle_validation_error(e):
    error_id = generate_error_id()
    log_error(e.messages, level="warning", error_id=error_id)
    return format_error(
        message="Validation failed for one or more fields.",
        code="VALIDATION_ERROR",
        error_id=error_id,
        details=e.messages
    ), 422

@errors.app_errorhandler(UnprocessableEntity)
def handle_unprocessable_entity(e):
    error_id = generate_error_id()
    log_error(e.description, level="warning", error_id=error_id)
    return format_error(
        message="The request was well-formed but could not be processed.",
        code="UNPROCESSABLE_ENTITY",
        error_id=error_id,
        details=e.data.get("messages") if hasattr(e, "data") else None
    ), 422

@errors.app_errorhandler(Exception)
def handle_generic_exception(e):
    error_id = generate_error_id()
    log_error(str(e), level="critical", error_id=error_id)
    return format_error("An unexpected error occurred.", "SERVER_ERROR", error_id=error_id), 500
