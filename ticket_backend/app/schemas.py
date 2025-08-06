from marshmallow import Schema, fields, validate

# User Schemas

class UserRegisterRequestSchema(Schema):
    name = fields.String(required=True, description="User's full name")
    email = fields.Email(required=True, description="User's email")
    password = fields.String(required=True, load_only=True, description="User's password")

class UserResponseSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    email = fields.Email(required=True)

class UserLoginRequestSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)

# Event Schemas

class EventResponseSchema(Schema):
    id = fields.String(required=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    datetime = fields.DateTime(required=True)
    venue = fields.String(required=True)

class EventListResponseSchema(Schema):
    events = fields.List(fields.Nested(EventResponseSchema))

# Seat Schemas

class SeatResponseSchema(Schema):
    id = fields.String(required=True)
    label = fields.String(required=True)
    status = fields.String(
        required=True,
        validate=validate.OneOf(["available", "booked"])
    )
    price = fields.Float(required=True)

class SeatListResponseSchema(Schema):
    seats = fields.List(fields.Nested(SeatResponseSchema))

# Ticket Schemas

class TicketResponseSchema(Schema):
    id = fields.String(required=True)
    event_id = fields.String(required=True)
    seat_id = fields.String(required=True)
    user_id = fields.String(required=True)
    booked_at = fields.DateTime(required=True)

class TicketListResponseSchema(Schema):
    tickets = fields.List(fields.Nested(TicketResponseSchema))

# Booking and Payment

class SeatBookRequestSchema(Schema):
    user_id = fields.String(required=True, description="User ID booking the seat")

class PaymentRequestSchema(Schema):
    user_id = fields.String(required=True)
    ticket_id = fields.String(required=True)
    card_number = fields.String(required=True, load_only=True)
    expiry = fields.String(required=True, load_only=True)
    cvc = fields.String(required=True, load_only=True)

class PaymentResponseSchema(Schema):
    id = fields.String(required=True)
    user_id = fields.String(required=True)
    ticket_id = fields.String(required=True)
    amount = fields.Float(required=True)
    status = fields.String(required=True)
    created_at = fields.DateTime(required=True)
