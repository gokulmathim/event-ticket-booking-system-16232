from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.schemas import (
    SeatListResponseSchema, SeatBookRequestSchema, TicketResponseSchema
)
from app import models

blp = Blueprint(
    "Seats", "seats", url_prefix="/events/<event_id>/seats",
    description="Seat selection and booking endpoints"
)

@blp.route("/")
class SeatList(MethodView):
    # PUBLIC_INTERFACE
    @blp.response(200, SeatListResponseSchema)
    def get(self, event_id):
        """List all seats for an event."""
        seats = models.list_seats(event_id)
        return {"seats": [
            {
                "id": seat["id"],
                "label": seat["label"],
                "status": seat["status"],
                "price": seat["price"]
            }
            for seat in seats
        ]}

@blp.route("/<seat_id>/book")
class SeatBook(MethodView):
    # PUBLIC_INTERFACE
    @blp.arguments(SeatBookRequestSchema)
    @blp.response(201, TicketResponseSchema)
    def post(self, body, event_id, seat_id):
        """Book a seat for an event (creates a ticket and updates seat status)."""
        user_id = body["user_id"]
        seat = models.get_seat(event_id, seat_id)
        if not seat:
            abort(404, message="Seat not found")
        if seat["status"] != "available":
            abort(409, message="Seat already booked")
        ticket = models.create_ticket(event_id, seat_id, user_id)
        if not ticket:
            abort(400, message="Unable to create ticket")
        return ticket
