from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.schemas import (
    PaymentRequestSchema, PaymentResponseSchema
)
from app import models

import random

blp = Blueprint(
    "Payments", "payments", url_prefix="/payments",
    description="Payment processing endpoints"
)

def mock_process_payment(card_number, expiry, cvc, amount):
    # Mock payment: random approve, just for demo!
    return random.choice([True, False])

@blp.route("/")
class PaymentCreate(MethodView):
    # PUBLIC_INTERFACE
    @blp.arguments(PaymentRequestSchema)
    @blp.response(201, PaymentResponseSchema)
    def post(self, payment_data):
        """Process payment for a ticket. If successful, status is 'completed', else 'failed'."""
        user_id = payment_data["user_id"]
        ticket_id = payment_data["ticket_id"]
        ticket = models.get_ticket(ticket_id)
        if not ticket or ticket["user_id"] != user_id:
            abort(404, message="Ticket not found or mismatch")
        amount = 0
        seat = models.get_seat(ticket["event_id"], ticket["seat_id"])
        if seat:
            amount = seat["price"]
        else:
            abort(400, message="Ticket seat missing")
        ok = mock_process_payment(
            payment_data["card_number"], payment_data["expiry"],
            payment_data["cvc"], amount
        )
        pay_status = "completed" if ok else "failed"
        payment = models.create_payment(
            user_id, ticket_id, amount, status=pay_status
        )
        return payment

@blp.route("/<payment_id>")
class PaymentDetail(MethodView):
    # PUBLIC_INTERFACE
    @blp.response(200, PaymentResponseSchema)
    def get(self, payment_id):
        """Get payment transaction status/details."""
        payment = models.get_payment(payment_id)
        if not payment:
            abort(404, message="Payment not found")
        return payment
