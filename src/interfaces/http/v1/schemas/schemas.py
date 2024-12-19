from marshmallow import Schema, fields

class CreateCustomerSchema(Schema):
    first_name = fields.String(required=True, validate=lambda x: 1 <= len(x) <= 50)
    last_name = fields.String(required=True, validate=lambda x: 1 <= len(x) <= 50)
    email = fields.Email(required=True)

class UpdateCustomerSchema(Schema):
    first_name = fields.String(validate=lambda x: 1 <= len(x) <= 50)
    last_name = fields.String(validate=lambda x: 1 <= len(x) <= 50)
    email = fields.Email()