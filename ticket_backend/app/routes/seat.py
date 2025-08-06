from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.schemas import (
    SeatListResponseSchema, SeatBookRequestSchema, TicketResponseSchema,
    MultiSeatBookRequestSchema, MultiTicketResponseSchema
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

@blp.route("/book")
class MultiSeatBook(MethodView):
    # PUBLIC_INTERFACE
    @blp.arguments(MultiSeatBookRequestSchema)
    @blp.response(201, MultiTicketResponseSchema)
    def post(self, req, event_id):
        """
        Book multiple seats atomically for an event.
        - Input: {"user_id": "...", "seat_ids": [seat_id1, seat_id2, ...]}
        - If any seat is already booked or not found, returns failed_seats list and no seats will be booked.
        - If all available, all booked, and tickets returned.
        """
        user_id = req["user_id"]
        seat_ids = req["seat_ids"]
        if not seat_ids or not isinstance(seat_ids, list):
            abort(400, message="seat_ids must be a list of seat IDs")
        booked_tickets, failed_seats = models.book_multiple_seats(event_id, seat_ids, user_id)
        if failed_seats and not booked_tickets:
            abort(409, message=f"One or more seats are already booked or not found: {failed_seats}")
        # Always atomic: either all or none, so failed_seats list will either be empty (success) or all failed.
        return {"tickets": booked_tickets, "failed_seats": failed_seats}
