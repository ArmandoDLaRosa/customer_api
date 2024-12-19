import os

from dependency_injector.wiring import Provide, inject
from flasgger import swag_from
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from infrastructure.container import Container
from interfaces.http.v1.schemas.schemas import (CreateCustomerSchema,
                                                UpdateCustomerSchema)
from webargs import fields
from webargs.flaskparser import use_args

bp = Blueprint("customers", __name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, '..', 'docs', 'customer')

@bp.route("/", methods=["GET"])
@use_args({
    "offset": fields.Int(missing=0, validate=lambda x: x >= 0),
    "limit": fields.Int(missing=10, validate=lambda x: 1 <= x <= 100),
}, location="query")
@swag_from(os.path.join(DOCS_DIR, 'list_customers.yml'))
@inject
def list_customers(data, use_cases=Provide[Container.use_cases]):
    offset = data["offset"]
    limit = data["limit"]
    customers = use_cases.list_customers_uc(offset=offset, limit=limit)
    return jsonify([customer.to_dict() for customer in customers]), 200

@bp.route('/<string:customer_id>', methods=['GET'])
@swag_from(os.path.join(DOCS_DIR, 'get_customer.yml'))
@inject
def get_customer(customer_id, use_cases=Provide[Container.use_cases]):
    customer = use_cases.get_customer_uc(customer_id)
    if not customer or customer.is_deleted:
        return jsonify({"error": "Not Found"}), 404
    return jsonify(customer.to_dict()), 200
  
@bp.route("/", methods=["POST"])
@use_args(CreateCustomerSchema, location="json")
@jwt_required()
@swag_from(os.path.join(DOCS_DIR, 'create_customer.yml'))
@inject
def create_customer(data, use_cases=Provide[Container.use_cases]):

    customer = use_cases.create_customer_uc(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
    )
    return jsonify(customer.to_dict()), 201


@bp.route('/<string:customer_id>', methods=["PUT"])
@use_args(UpdateCustomerSchema, location="json", as_kwargs=True)
@swag_from(os.path.join(DOCS_DIR, 'update_customer.yml'))
@inject
def update_customer(customer_id, *, use_cases=Provide[Container.use_cases], **data):
    customer = use_cases.update_customer_uc(
        customer_id=customer_id,
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        email=data.get("email"),
    )
    return jsonify(customer.to_dict()), 200
  
@bp.route('/<string:customer_id>', methods=['DELETE'])
@jwt_required()
@swag_from(os.path.join(DOCS_DIR, 'delete_customer.yml'))
@inject
def delete_customer(customer_id, use_cases=Provide[Container.use_cases]):
    use_cases.delete_customer_uc(customer_id)
    return '', 204
